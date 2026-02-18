import os
import uuid
import random
from fastapi import FastAPI, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- QUESTIONS ----------------
QUESTIONS = {
    "easy": [
        "What is {domain}?",
        "Why is {domain} used?",
        "Explain basics of {domain}."
    ],
    "medium": [
        "How does {domain} work internally?",
        "Explain components of {domain}.",
        "Advantages and disadvantages of {domain}?"
    ],
    "hard": [
        "Design scalable system using {domain}.",
        "Advanced challenges in {domain}?",
        "Compare {domain} with alternatives."
    ]
}

sessions = {}

# ---------------- START ----------------
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
        "question": question,
        "difficulty": "easy"
    }

# ---------------- ANSWER (JSON TEXT VERSION) ----------------
@app.post("/answer")
async def answer(payload: dict = Body(...)):

    session_id = payload.get("session_id")
    text = payload.get("answer_text")

    if not session_id or not text:
        return {"error": "Missing session_id or answer_text"}

    session = sessions.get(session_id)
    if not session:
        return {"error": "Invalid session"}

    text = text.strip()
    if not text:
        return {"error": "Empty answer"}

    # Evaluate using Groq LLM
    evaluation = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an interview evaluator."},
            {"role": "user", "content": f"Evaluate this answer: {text}. Respond only with: poor, average, or good."}
        ]
    )

    performance = evaluation.choices[0].message.content.lower()

    session["answers"].append({
        "answer": text,
        "performance": performance
    })

    session["questions_asked"] += 1

    # Interview finished
    if session["questions_asked"] >= session["max_questions"]:

        final_eval = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an interview evaluator."},
                {"role": "user", "content": f"Give final feedback for these answers: {session['answers']}"}
            ]
        )

        return {
            "answer_text": text,
            "final_feedback": final_eval.choices[0].message.content,
            "interview_completed": True
        }

    # Increase difficulty if good
    if "good" in performance:
        if session["level"] == "easy":
            session["level"] = "medium"
        elif session["level"] == "medium":
            session["level"] = "hard"

    next_q = random.choice(
        QUESTIONS[session["level"]]
    ).format(domain=session["domain"])

    return {
        "answer_text": text,
        "next_question": next_q,
        "difficulty": session["level"],
        "interview_completed": False
    }
