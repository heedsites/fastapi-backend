import os
import json
import re
from groq import Groq

# Canonical concept mapping
CONCEPT_ALIASES = {
    "oop": "OOP",
    "object oriented programming": "OOP",
    "object-oriented programming": "OOP",
    "object-oriented programming (oop) principles": "OOP",
    "classes and objects": "OOP",
    "inheritance": "OOP",
    "polymorphism": "OOP",
    "encapsulation": "OOP",
    "object-oriented programming (inheritance)": "OOP",
    "oop principles": "OOP",
    "inheritance concept": "OOP",
    "oop inheritance": "OOP",


    "loops": "Loops",
    "loop": "Loops",
    "for loop": "Loops",
    "while loop": "Loops",
    "control structures": "Loops",

    "list comprehension": "List Comprehension",
    "lists": "List Comprehension",

    "recursion": "Recursion",
    "functions": "Functions",
    "strings": "Strings",
    "arrays": "Arrays"
}


def normalize_concept(concept: str) -> str:
    key = concept.strip().lower()
    return CONCEPT_ALIASES.get(key, concept.strip().title())

class QuestionAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _extract_json(self, text: str) -> dict:
        """
        Safely extract JSON from LLM response
        """
        try:
            # find JSON block
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if not match:
                raise ValueError("No JSON found in AI response")

            json_str = match.group(0)
            return json.loads(json_str)

        except Exception as e:
            raise ValueError(f"Invalid AI JSON output: {text}") from e

    def classify_question(self, question_text: str) -> dict:
        """
        Analyze a question and return domain, concept and difficulty
        """

        prompt = f"""
You are an academic question classifier.

Analyze the following question and return STRICT JSON only.

Question:
{question_text}

Return ONLY JSON:
{{
  "domain": "Python / Java / DSA / Aptitude / SQL / Other",
  "concept": "specific topic",
  "difficulty": "Easy / Medium / Hard"
}}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw_output = response.choices[0].message.content.strip()

        data=self._extract_json(raw_output)
        data["concept"] = normalize_concept(data["concept"])
        return data
