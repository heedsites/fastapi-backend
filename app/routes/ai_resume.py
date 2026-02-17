from fastapi import APIRouter
from app.models.ai_resume import ResumeRequest, ResumeResponse
from app.controllers.ai_resume import generate_resume

router = APIRouter(prefix="/ai_resume", tags=["AI Resume"])


@router.post("/generate", response_model=ResumeResponse)
async def create_resume(data: ResumeRequest):
    return await generate_resume(data)
