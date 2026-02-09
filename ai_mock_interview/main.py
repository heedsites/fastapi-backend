import subprocess
import os
import tempfile
import uuid
import random
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- QUESTIONS BY DIFFICULTY ----------------
QUESTIONS = {
    "easy": [
        "What is {domain}?",
        "Explain the basics of {domain}.",
        "Why is {domain} used?"
    ],
    "medium": [
        "How does {domain} work?",
        "What are key components of {domain}?",
        "Explain advantages and disadvantages of {domain}."
    ],
    "hard": [
        "Explain advanced challenges in {domain}.",
        "How would you design a scalable system using {domain}?",
        "Compare {domain} with an alternative approach."
    ]
}

sessions = {}

# ---------------- UTILS ----------------
def evaluate_answer(answer: str):
    words = len(answer.split())
    if words < 5:
        return "poor"
    if words >= 15 or "example" in answer.lower():
        return "good"
    return "average"

def next_level(current, performance):
    if performance == "good":
        if current == "easy":
            return "medium"
        if current == "medium":
            return "hard"
    return current

def final_feedback(answers):
    good = sum(1 for a in answers if a["performance"] == "good")
    total = len(answers)

    if good >= total * 0.7:
        return "Strong performance. You showed good understanding and confidence."
    elif good >= total * 0.4:
        return "Average performance. Improve depth and clarity."
    return "Needs improvement. Revise fundamentals and practice."

# ---------------- FFmpeg CHECK ----------------
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

if not check_ffmpeg():
    raise RuntimeError("FFmpeg not found! Add it to PATH.")

# ---------------- START INTERVIEW ----------------
@app.post("/start")
def start(domain: str = Form(...)):
    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "domain": domain,
        "level": "easy",
        "questions_asked": 0,
        "answers": [],
        "max_questions": 5
    }

    question = random.choice(QUESTIONS["easy"]).format(domain=domain)

    return {
        "session_id": session_id,
        "question": question
    }

# ---------------- ANSWER ----------------
@app.post("/answer")
def answer(session_id: str = Form(...), audio: UploadFile = File(...)):
    session = sessions.get(session_id)
    if not session:
        return {"error": "Invalid session"}

    # Save audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(audio.file.read())
        webm_path = tmp.name

    wav_path = webm_path.replace(".webm", ".wav")

    # Convert to wav
    subprocess.run(
        ["ffmpeg", "-y", "-i", webm_path, "-ar", "16000", "-ac", "1", wav_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Speech to text
    r = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    except Exception:
        text = ""
    finally:
        os.remove(webm_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)

    if not text:
        return {"error": "Speech not recognized"}

    # Evaluate
    performance = evaluate_answer(text)

    session["answers"].append({
        "answer": text,
        "performance": performance
    })

    session["questions_asked"] += 1

    # Interview finished
    if session["questions_asked"] >= session["max_questions"]:
        feedback = final_feedback(session["answers"])
        return {
            "answer_text": text,
            "final_feedback": feedback,
            "interview_completed": True
        }

    # Adjust difficulty
    session["level"] = next_level(session["level"], performance)

    next_q = random.choice(
        QUESTIONS[session["level"]]
    ).format(domain=session["domain"])

    return {
        "answer_text": text,
        "next_question": next_q,
        "difficulty": session["level"],
        "interview_completed": False
    }
