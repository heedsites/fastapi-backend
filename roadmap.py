import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from groq import Groq

app = FastAPI(title="Arikya AI Placement API")
client = Groq(api_key='')

class StudentData(BaseModel):
    branch: str
    cgpa: float = Field(..., ge=0, le=10)
    targets: List[str]
    coding_score: int = Field(..., ge=0, le=100)
    aptitude_score: int = Field(..., ge=0, le=100)
    feedback: str
def get_ai_roadmap(data: StudentData):
    system_prompt = (
        "You are Arikya AI, a placement roadmap generator. "
        "Your goal is to convert student performance data into a clear, "
        "actionable, time-bound roadmap. Focus on practicality and placement success."
    )

    user_prompt = f"""
    Generate a 6-week personalized placement roadmap:
    - Branch: {data.branch}
    - CGPA: {data.cgpa}
    - Target Companies: {', '.join(data.targets)}
    - Coding: {data.coding_score}% | Aptitude: {data.aptitude_score}%
    - Feedback: {data.feedback}
    
    Structure the output by Week, including daily tasks and a weekend measurable outcome.
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/generate-roadmap")
async def create_roadmap(student: StudentData):
    roadmap_text = get_ai_roadmap(student)
    return {
        "status": "success",
        "roadmap": roadmap_text
    }