import os
import json
import requests

from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS

from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip
)

from PIL import Image


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

HF_KEY = os.getenv("HF_API_KEY")

CHARACTER_STYLE = """
A golden lion with thick dark mane, amber eyes,
A small grey mouse with round ears,
Pixar style animation, soft lighting
"""


def generate_scenes(text: str):

    prompt = f"""
Create 2 scenes. Return ONLY JSON.

[
  {{
    "scene_id": 1,
    "narration": "...",
    "image_prompt": "..."
  }}
]

Topic: {text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_output = response.choices[0].message.content

    start = raw_output.find("[")
    end = raw_output.rfind("]") + 1

    scenes = json.loads(
        raw_output[start:end]
    )

    return scenes


def generate_image(
    prompt: str,
    scene_id: int
):

    os.makedirs("media", exist_ok=True)

    full_prompt = prompt

    API_URL = (
        "https://router.huggingface.co/hf-inference/models/"
        "black-forest-labs/FLUX.1-schnell"
    )

    headers = {
        "Authorization": f"Bearer {HF_KEY}"
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": full_prompt
        },
        timeout=60
    )

    print("HF STATUS:", response.status_code)

    image_path = f"media/{scene_id}.png"

    if response.status_code == 200:

        with open(image_path, "wb") as file:
            file.write(response.content)

        image = (
            Image.open(image_path)
            .resize((1280, 720))
        )

        image.save(image_path)

        print(
            f"Image {scene_id} generated"
        )

    else:

        print("HF ERROR:")
        print(response.text)

        fallback = Image.new(
            "RGB",
            (1280, 720),
            (
                40 * scene_id % 255,
                70 * scene_id % 255,
                100 * scene_id % 255
            )
        )

        fallback.save(image_path)

    return image_path


def create_audio(scenes: list):

    os.makedirs("output", exist_ok=True)

    narration_text = " ".join(
        scene["narration"]
        for scene in scenes
    )

    audio_path = "output/audio.mp3"

    gTTS(narration_text).save(audio_path)

    return audio_path, narration_text


def create_motion_clip(
    image_path: str,
    duration: float,
    index: int
):

    clip = (
        ImageClip(image_path)
        .set_duration(duration)
    )

    clip = clip.resize(
        lambda t: 1 + 0.06 * t
    )

    if index % 2 == 0:

        clip = clip.set_position(
            lambda t: ("center", -20 * t)
        )

    else:

        clip = clip.set_position(
            lambda t: ("center", 20 * t)
        )

    return clip


def create_video(scenes: list):

    audio_path, narration_text = create_audio(
        scenes
    )

    audio = AudioFileClip(audio_path)

    scene_clips = []

    per_scene_duration = (
        audio.duration / len(scenes)
    )

    for index, scene in enumerate(scenes):

        image_path = generate_image(
            scene["image_prompt"],
            scene["scene_id"]
        )

        motion_clip = create_motion_clip(
            image_path,
            per_scene_duration,
            index
        )

        scene_clips.append(
            motion_clip
        )

    video = concatenate_videoclips(
        scene_clips,
        method="compose"
    )

    final_video = (
        CompositeVideoClip([video])
        .set_audio(audio)
        .set_duration(audio.duration)
    )

    output_path = "output/final.mp4"

    final_video.write_videofile(
        output_path,
        fps=12
    )

    return output_path