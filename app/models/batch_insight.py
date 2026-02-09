from pydantic import BaseModel
from typing import List
from app.models.top_performers import Submission


class BatchInsightRequest(BaseModel):
    submissions: List[Submission]
