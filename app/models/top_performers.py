from pydantic import BaseModel
from typing import List, Dict


class Submission(BaseModel):
    student_id: str
    question: str
    is_correct: bool


class TopPerformersRequest(BaseModel):
    submissions: List[Submission]
    top_n: int = 10


class TopPerformer(BaseModel):
    student_id: str
    overall_score: float
    concept_breakdown: Dict[str, float]
