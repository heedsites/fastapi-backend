from pydantic import BaseModel
from typing import List
from app.models.top_performers import Submission


class DashboardQueryRequest(BaseModel):
    question: str
    submissions: List[Submission]
