from typing import List
from fastapi import APIRouter
import os
import requests

router = APIRouter(prefix="/admin", tags=["AI Dashboard"])

# --------------------
# Dummy data (for now)
# --------------------
students = [
    {"mail": "aryan@gmail.com", "name": "Aryan"},
    {"mail": "sneha@gmail.com", "name": "Sneha"},
    {"mail": "rahul@gmail.com", "name": "Rahul"},
]

code_ratings = [
    {"mail": "aryan@gmail.com", "topic": "Python Basics", "marks": 85},
    {"mail": "sneha@gmail.com", "topic": "Python Basics", "marks": 45},
    {"mail": "rahul@gmail.com", "topic": "Python Basics", "marks": 30},
]

# --------------------
# APIs
# --------------------
@router.get("/top-students")
def top_students(n: int = 3):
    result = []
    for r in code_ratings:
        for s in students:
            if s["mail"] == r["mail"]:
                result.append({
                    "name": s["name"],
                    "mail": s["mail"],
                    "marks": r["marks"]
                })
    result.sort(key=lambda x: x["marks"], reverse=True)
    return result[:n]


@router.get("/weak-students")
def weak_students(threshold: int = 40):
    result = []
    for r in code_ratings:
        if r["marks"] < threshold:
            for s in students:
                if s["mail"] == r["mail"]:
                    result.append({
                        "name": s["name"],
                        "mail": s["mail"],
                        "marks": r["marks"]
                    })
    return result


@router.get("/skill-distribution")
def skill_distribution():
    skills = {"python": 0, "frontend": 0, "backend": 0}
    for r in code_ratings:
        if r["marks"] >= 50 and "python" in r["topic"].lower():
            skills["python"] += 1
    return skills


@router.get("/ai-summary")
def ai_summary():
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    prompt = f"""
Top Students: {top_students()}
Weak Students: {weak_students()}
Skill Distribution: {skill_distribution()}

Give a short placement summary.
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )

    return {
        "summary": response.json()["choices"][0]["message"]["content"]
    }
