import os
import json
from groq import Groq
from dotenv import load_dotenv
from fastapi import HTTPException

from app.models.coding_questions import QuestionRequest

# Load environment variables
load_dotenv()

GROQ_MODEL = "llama-3.1-8b-instant"
_client = None


def _get_groq_client():
    """Lazy initialization of Groq client."""
    global _client
    if _client is None:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY environment variable is not set. Please configure it in Vercel environment variables."
            )
        _client = Groq(api_key=groq_api_key)
    return _client


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
    try:
        client = _get_groq_client()
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize Groq client: {str(e)}"
        )

    prompt = _build_prompt(req.topic, req.difficulty, req.language)

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Return strict JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Groq API request failed: {str(e)}"
        )

    content = response.choices[0].message.content
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse Groq response as JSON: {str(e)}\nRaw content: {content[:200]}"
        )

    # Validate required keys
    missing_keys = [key for key in REQUIRED_KEYS if key not in data]
    if missing_keys:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required keys in response: {', '.join(missing_keys)}"
        )

    return data