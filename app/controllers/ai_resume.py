import os
import json
from groq import Groq
from fastapi import HTTPException
from app.models.ai_resume import ResumeRequest, ResumeResponse

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(data: ResumeRequest) -> str:
    project_lines = "\n".join(
        [f"{p.title}: {p.description}" for p in data.projects]
    )

    return f"""
You are an expert resume writer.

Generate a professional ATS optimized resume content.

Name: {data.student_name}
Target Role: {data.target_role}
Education: {data.education}

Skills: {', '.join(data.skills)}

Quiz Performance:
{data.quiz_performance}

Coding Practice:
Solved {data.coding_stats.problems_solved} problems
Topics: {', '.join(data.coding_stats.topics)}

Projects:
{project_lines}

Return STRICT JSON format:
{{
 "summary": "",
 "experience_points": [],
 "project_descriptions": [],
 "skill_highlights": [],
 "suggestions": []
}}
"""


async def generate_resume(data: ResumeRequest) -> ResumeResponse:

    prompt = build_prompt(data)

    completion = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=[
            {"role": "system", "content": "You ONLY return valid JSON. No explanation. No markdown."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = completion.choices[0].message.content

    # ---- JSON SAFETY EXTRACTION ----
    try:
        parsed = json.loads(content)
    except Exception:
        start = content.find("{")
        end = content.rfind("}") + 1
        json_str = content[start:end]

        try:
            parsed = json.loads(json_str)
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="AI failed to generate structured resume. Try again."
            )

    # ---- RESPONSE VALIDATION ----
    try:
        return ResumeResponse(**parsed)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="AI response structure mismatch"
        )
