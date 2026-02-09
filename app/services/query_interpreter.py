import os
import json
import re
from groq import Groq


class QueryInterpreter:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _extract_json(self, text: str):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            raise ValueError("Invalid AI response")
        return json.loads(match.group(0))

    def interpret(self, question: str):
        prompt = f"""
You are an academic dashboard assistant.

Convert the faculty question into structured JSON.

Question:
{question}

Return JSON ONLY:

{{
 "intent": "top_performers | batch_insight",
 "subject": "python/java/dsa/aptitude/unknown",
 "limit": number_or_10_default
}}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return self._extract_json(response.choices[0].message.content.strip())
