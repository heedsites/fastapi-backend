import os
import json
from groq import Groq
from dotenv import load_dotenv

from app.models.coding_questions import QuestionRequest

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found")

client = Groq(api_key=GROQ_API_KEY)
GROQ_MODEL = "llama-3.1-8b-instant"

REQUIRED_KEYS = [
    "question", "constraints", "input_format", "output_format",
    "sample_input", "sample_output", "test_cases",
]


def _build_prompt(topic: str, difficulty: str, language: str) -> str:
    return f"""
You are an API that generates coding questions.

Topic: {topic}
Difficulty: {difficulty}
Language: {language}

Respond ONLY with valid JSON.
NO markdown.
NO explanation.
NO extra text.

STRICT JSON FORMAT:
{{
  "question": "string",
  "constraints": "string",
  "input_format": "string",
  "output_format": "string",
  "sample_input": "string",
  "sample_output": "string",
  "test_cases": [
    {{
      "input": "string",
      "output": "string"
    }}
  ]
}}
"""


def generate_question(req: QuestionRequest) -> dict:
    """Generate a coding question via Groq."""
    prompt = _build_prompt(req.topic, req.difficulty, req.language)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "Return strict JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Groq response: {e}\nRaw: {content}")

    for key in REQUIRED_KEYS:
        if key not in data:
            raise ValueError(f"Missing key in response: {key}")

    return data
