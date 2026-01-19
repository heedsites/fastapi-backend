import os
import json
import time
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from groq import Groq
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

from PIL import Image, ImageDraw, ImageFont

# ======================================================
# ENV SETUP
# ======================================================
load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
HF_KEY = os.getenv("HF_API_KEY")

if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY missing in .env")
if not HF_KEY:
    raise RuntimeError("HF_API_KEY missing in .env")

client = Groq(api_key=GROQ_KEY)

# ======================================================
# FASTAPI APP
# ======================================================
app = FastAPI(title="Text to Video with Captions (Stable)")

# ======================================================
# INPUT MODEL
# ======================================================
class VideoRequest(BaseModel):
    text: str

# ======================================================
# GROQ: SCENE + IMAGE PROMPT GENERATION
# ======================================================
def generate_scenes(text: str):
    prompt = f"""
You are creating a YouTube Shorts educational explainer video
lasting 30–40 seconds.

RULES:
- Create 5 short scenes
- Each scene must explain the concept step by step
- Clear, student-friendly language
- No emojis
- No markdown
- Output ONLY valid JSON

Each scene must include:
scene_id,
narration (1–2 sentences),
image_prompt (descriptive visual),
duration (4 to 8 seconds)

FORMAT:
[
  {{
    "scene_id": 1,
    "narration": "short hook",
    "image_prompt": "visual description",
    "duration": 5
  }}
]

TOPIC:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    raw = response.choices[0].message.content.strip()

    if not raw.startswith("["):
        raise RuntimeError(f"Groq returned invalid JSON: {raw}")

    return json.loads(raw)

# ======================================================
# HUGGING FACE IMAGE GENERATION (ROUTER + RETRY)
# ======================================================
def generate_image(prompt: str, scene_id: int, retries: int = 3):
    os.makedirs("media", exist_ok=True)

    url = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {
        "Authorization": f"Bearer {HF_KEY}",
        "Content-Type": "application/json"
    }

    for attempt in range(1, retries + 1):
        response = requests.post(
            url,
            headers=headers,
            json={"inputs": prompt},
            timeout=120
        )

        # SUCCESS → IMAGE
        if (
            response.status_code == 200
            and response.headers.get("content-type", "").startswith("image")
        ):
            image_path = f"media/scene_{scene_id}.png"
            with open(image_path, "wb") as f:
                f.write(response.content)
            return image_path

        # HF often returns JSON error / busy
        time.sleep(10)

    raise RuntimeError("Image generation failed (HF busy or blocked)")

# ======================================================
# ADD CAPTIONS (SAFE PIL VERSION)
# ======================================================
def add_text_to_image(image_path: str, text: str, scene_id: int):
    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        raise RuntimeError(f"Image open failed: {e}")

    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Caption bar
    bar_height = 120
    draw.rectangle(
        [(0, height - bar_height), (width, height)],
        fill=(0, 0, 0)
    )

    # Always-safe font
    font = ImageFont.load_default()

    # Limit text length
    text = text[:160]

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = max((width - text_width) // 2, 10)
    y = height - bar_height + (bar_height - text_height) // 2

    draw.text((x, y), text, fill=(255, 255, 255), font=font)

    out_path = f"media/captioned_{scene_id}.png"
    img.save(out_path)

    return out_path

# ======================================================
# SINGLE CONTINUOUS AUDIO
# ======================================================
def create_full_audio(scenes):
    os.makedirs("output", exist_ok=True)

    full_text = " ".join(scene["narration"] for scene in scenes)
    audio_path = "output/narration.mp3"

    gTTS(full_text).save(audio_path)
    return audio_path

# ======================================================
# VIDEO CREATION
# ======================================================
def create_video(scenes):
    os.makedirs("output", exist_ok=True)
    clips = []

    narration_audio_path = create_full_audio(scenes)
    narration_audio = AudioFileClip(narration_audio_path)

    for scene in scenes:
        img = generate_image(scene["image_prompt"], scene["scene_id"])
        img = add_text_to_image(img, scene["narration"], scene["scene_id"])

        clip = (
            ImageClip(img)
            .set_duration(scene["duration"])
            .resize(height=720)
        )

        clips.append(clip)

    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.set_audio(narration_audio)

    final_video.write_videofile(
        "output/final_video.mp4",
        fps=24
    )

# ======================================================
# API ENDPOINT (NO BLIND 500)
# ======================================================
@app.post("/generate-video")
def generate_video(req: VideoRequest):
    try:
        scenes = generate_scenes(req.text)
        create_video(scenes)
        return {
            "status": "success",
            "output": "output/final_video.mp4"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
