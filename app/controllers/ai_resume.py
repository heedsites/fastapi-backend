import os
import json
from groq import Groq
from fastapi import HTTPException
from app.models.ai_resume import ResumeRequest, ResumeResponse
from app.services.mock_student_profile import get_student_profile

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------- PROMPT ----------------
def build_prompt(data: ResumeRequest) -> str:
    project_lines = "\n".join(
        [f"{p.title}: {p.description}" for p in data.projects]
    )

    return f"""
Write a professional fresher software engineer resume content.

Candidate:
Role: {data.target_role}
Education: {data.education}
Skills: {', '.join(data.skills)}
Solved {data.coding_stats.problems_solved} problems in {', '.join(data.coding_stats.topics)}
Concept areas: {data.quiz_performance}

Projects:
{project_lines}

Write professionally like industry resume bullet points.
No suggestions. No scores. No explanation.
"""


# ---------------- JSON FORMATTER ----------------
def format_to_json(raw_text: str) -> dict:

    schema_instruction = f"""
Convert the following resume content into STRICT JSON.

Return ONLY JSON. No markdown.

JSON format:
{{
 "professional_summary": "",
 "technical_skills": [],
 "experience_highlights": [],
 "project_details": []
}}

CONTENT:
{raw_text}
"""

    completion = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=[
            {"role": "system", "content": "You output only valid JSON."},
            {"role": "user", "content": schema_instruction}
        ],
        temperature=0
    )

    content = completion.choices[0].message.content

    start = content.find("{")
    end = content.rfind("}") + 1
    json_str = content[start:end]

    return json.loads(json_str)
def improve_bullet(text: str) -> str:
    text = text.strip()

    replacements = [
        ("Solved", "Implemented solutions for"),
        ("Demonstrated ability to", "Developed capability to"),
        ("Worked on", "Developed"),
        ("Used", "Utilized"),
        ("Learned", "Applied"),
    ]

    for old, new in replacements:
        if text.lower().startswith(old.lower()):
            text = new + text[len(old):]

    # remove useless lines
    if len(text.split()) <= 2:
        return None

    return text

def improve_experience_line(text: str) -> str:
    text = text.strip()

    weak_starters = [
        "Proficient in",
        "Familiarity with",
        "Strong understanding of",
        "Knowledge of"
    ]

    for phrase in weak_starters:
        if text.startswith(phrase):
            skill = text.replace(phrase, "").strip()
            return f"Applied {skill} in practical development scenarios"

    return text


def clean_project_line(text: str) -> str:
    text = text.strip()

    # Case 1: dict-like string → convert
    if text.startswith("{") and "description" in text:
        try:
            import ast
            data = ast.literal_eval(text)
            name = data.get("project_name", "Project")
            desc = data.get("description", "")
            return f"Developed {name} — {desc}"
        except:
            return text

    # Case 2: model already wrote good sentence → keep it
    if len(text.split()) > 6:
        return text

    # Case 3: too short → drop
    return None

def remove_weak_lines(lines):
    cleaned = []
    for line in lines:
        l = line.lower().strip()

        # remove job titles
        if "fresher" in l:
            continue
        if l in ["backend developer", "software developer", "developer"]:
            continue

        # remove single skill-like statements
        if len(l.split()) <= 3:
            continue
        if "system" in l and "management" in l:
            continue

        cleaned.append(line)

    return cleaned


async def generate_resume(data: ResumeRequest) -> ResumeResponse:

    # 1️⃣ Generate resume text
    completion = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=[
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": build_prompt(data)}
        ],
        temperature=0.3
    )

    raw_text = completion.choices[0].message.content

    # 2️⃣ Convert to JSON using LLM formatter
    try:
        structured = format_to_json(raw_text)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to structure AI output")

    # 3️⃣ NORMALIZATION HELPERS
    def ensure_list(value):
        if isinstance(value, list):
            return [str(v).strip() for v in value if str(v).strip()]
        if isinstance(value, str):
            lines = [v.strip("-• \n\t") for v in value.replace(",", "\n").split("\n")]
            return [l for l in lines if l]
        return []

    def improve_bullet(text: str):
        text = text.strip()

        replacements = [
            ("Solved", "Implemented solutions for"),
            ("Demonstrated ability to", "Developed capability to"),
            ("Worked on", "Developed"),
            ("Used", "Utilized"),
            ("Learned", "Applied"),
        ]

        for old, new in replacements:
            if text.lower().startswith(old.lower()):
                text = new + text[len(old):]

        if len(text.split()) <= 2:
            return None

        return text

    # 4️⃣ Normalize fields
    skills = ensure_list(structured.get("technical_skills", []))

    exp = ensure_list(structured.get("experience_highlights", []))
    exp = [improve_bullet(e) for e in exp]
    exp = [improve_experience_line(e) for e in exp if e]
    exp = remove_weak_lines(exp)
    projects = ensure_list(structured.get("project_details", []))
    projects = [clean_project_line(p) for p in projects]
    projects = [p for p in projects if p]

    normalized = {
        "professional_summary": str(structured.get("professional_summary", "")),
        "technical_skills": skills,
        "experience_highlights": exp,
        "project_details": projects,
    }

    # 5️⃣ Final validation
    try:
        profile = get_student_profile(data.student_name)
        final_response = {
            **normalized,
            "education": profile["education"],
            "certifications": profile["certifications"],
            "work_experience": profile["work_experience"],
        }
        return ResumeResponse(**final_response)

    except Exception as e:
        print("STRUCTURED:", structured)
        print("NORMALIZED:", normalized)
        raise HTTPException(status_code=500, detail="AI structure normalization failed")
