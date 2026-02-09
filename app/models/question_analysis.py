from pydantic import BaseModel


class QuestionAnalysisRequest(BaseModel):
    question: str


class QuestionAnalysisResponse(BaseModel):
    domain: str
    concept: str
    difficulty: str
