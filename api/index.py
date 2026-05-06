# ==============================
# IMPORTS
# ==============================
import os
import json
import requests
import torch
import numpy as np

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from groq import Groq
from gtts import gTTS
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip,
    TextClip
)
from PIL import Image

import deepinv as dinv

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello"}

# ==============================
# ENV
# ==============================
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
HF_KEY = os.getenv("HF_API_KEY")

app = FastAPI(title="AI Video Generator")

class VideoRequest(BaseModel):
    text: str

# ==============================
# LOAD DEEPINV MODEL
# ==============================
device = "cpu"
denoise_model = dinv.models.DnCNN(pretrained="download").to(device)

# ==============================
# STYLE
# ==============================
CHARACTER_STYLE = """
A golden lion with thick dark mane, amber eyes,
A small grey mouse with round ears,
Pixar style animation, soft lighting
"""

# ==============================
# SCENES
# ==============================
def generate_scenes(text):
    prompt = f"""
Create 6 scenes. Return ONLY JSON.

[
  {{
    "scene_id": 1,
    "narration": "...",
    "image_prompt": "..."
  }}
]

Topic: {text}
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Return only JSON"},
            {"role": "user", "content": prompt}
        ]
    )

    raw = res.choices[0].message.content
    start = raw.find("[")
    end = raw.rfind("]") + 1

    scenes = json.loads(raw[start:end])

    return scenes

# ==============================
# IMAGE GENERATION
# ==============================
def generate_image(prompt, sid):
    os.makedirs("media", exist_ok=True)

    url = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {HF_KEY}"}

    full_prompt = CHARACTER_STYLE + "\n" + prompt

    r = requests.post(url, headers=headers, json={"inputs": full_prompt})

    path = f"media/{sid}.png"

    if r.status_code == 200:
        with open(path, "wb") as f:
            f.write(r.content)

        img = Image.open(path).resize((1280, 720))
        img.save(path)
    else:
        img = Image.new("RGB", (1280, 720), (30, 30, 30))
        img.save(path)

    return path

# ==============================
# DEEPINV ENHANCEMENT
# ==============================
def enhance_image(img_path):
    img = Image.open(img_path).convert("RGB").resize((256, 256))

    img_np = np.array(img) / 255.0
    img_tensor = torch.tensor(img_np).permute(2, 0, 1).unsqueeze(0).float()

    with torch.no_grad():
        output = denoise_model(img_tensor)

    out = output.squeeze().permute(1, 2, 0).numpy()
    out = (out * 255).clip(0, 255).astype("uint8")

    enhanced = Image.fromarray(out).resize((1280, 720))

    new_path = img_path.replace(".png", "_enhanced.png")
    enhanced.save(new_path)

    return new_path

# ==============================
# AUDIO
# ==============================
def create_audio(scenes):
    os.makedirs("output", exist_ok=True)

    text = " ".join(s["narration"] for s in scenes)
    path = "output/audio.mp3"

    gTTS(text).save(path)
    return path, text

# ==============================
# MOTION ENGINE
# ==============================
def create_motion_clip(img_path, duration, i):
    base = ImageClip(img_path).set_duration(duration)

    base = base.resize(lambda t: 1 + 0.06 * t)

    if i % 2 == 0:
        base = base.set_position(lambda t: ("center", -20 * t))
    else:
        base = base.set_position(lambda t: ("center", 20 * t))

    return base

# ==============================
# AUDIO-SYNCED CAPTIONS
# ==============================
def generate_timed_captions(audio, text):
    words = text.split()

    total_duration = audio.duration
    time_per_word = total_duration / len(words)

    captions = []
    current_time = 0

    chunk_size = 4

    for i in range(0, len(words), chunk_size):
        chunk = words[i:i+chunk_size]
        line = " ".join(chunk)

        start = current_time
        end = start + len(chunk) * time_per_word

        captions.append((start, end, line))

        current_time = end

    return captions


def create_subtitle_clips(captions):
    clips = []

    for start, end, text in captions:
        txt = TextClip(
            text,
            fontsize=40,
            color="white",
            method="caption",
            size=(1000, None)
        )

        txt = txt.set_start(start).set_end(end)
        txt = txt.set_position(("center", 600))

        clips.append(txt)

    return clips

# ==============================
# VIDEO
# ==============================
def create_video(scenes):
    audio_path, full_text = create_audio(scenes)
    audio = AudioFileClip(audio_path)

    captions = generate_timed_captions(audio, full_text)
    subtitle_clips = create_subtitle_clips(captions)

    clips = []

    per_scene_duration = audio.duration / len(scenes)

    for i, s in enumerate(scenes):
        img = generate_image(s["image_prompt"], s["scene_id"])
        img = enhance_image(img)

        clip = create_motion_clip(img, per_scene_duration, i)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    final = CompositeVideoClip([video] + subtitle_clips)

    final = final.set_audio(audio).set_duration(audio.duration)

    final.write_videofile("output/final.mp4", fps=12)

# ==============================
# API
# ==============================
@app.post("/generate")
def generate(req: VideoRequest):
    try:
        scenes = generate_scenes(req.text)
        create_video(scenes)

        return {"status": "success", "video": "output/final.mp4"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
