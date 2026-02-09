import os
import json
from groq import Groq


class InsightGenerator:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_student_summary(self, student_data: dict) -> str:
        prompt = f"""
You are an academic performance analyst.

Given a student's concept performance, write a short professional performance summary for faculty.

Data:
{student_data}

Rules:
- 2 to 3 lines
- Mention strengths
- Mention weaknesses
- Do not repeat numeric scores
- Clear academic tone
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()
    def generate_batch_summary(self, batch_data: dict) -> str:
        data_json = json.dumps(batch_data, indent=2)

        prompt = f"""
You are an academic performance analyst.

Generate a concise batch performance summary for faculty.

Batch Data (JSON):
{data_json}

Rules:
- 2 to 3 lines
- Mention strong areas
- Mention weak or moderate areas
- Professional academic tone
"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print("Groq error:", e)
            return "Batch performance summary unavailable due to AI service error."
