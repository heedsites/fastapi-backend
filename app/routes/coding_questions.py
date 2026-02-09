from fastapi import APIRouter, HTTPException, status

from app.models.coding_questions import QuestionRequest, QuestionResponse
from app.controllers.coding_questions import generate_question

router = APIRouter(tags=["Coding Questions"])


@router.post(
    "/generate-question",
    summary="Generate Coding Question",
    description="Generate a coding question using AI based on topic, difficulty, and language",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successfully generated coding question",
            "model": QuestionResponse,
        },
        500: {"description": "Server error or failed to generate question"},
        503: {"description": "Service unavailable - API key not configured"},
    },
)
def generate_question_route(req: QuestionRequest):
    """
    Generate a coding question.
    
    - **topic**: The topic/subject of the coding question (e.g., "arrays", "sorting")
    - **difficulty**: Difficulty level (e.g., "easy", "medium", "hard")
    - **language**: Programming language (e.g., "python", "c", "cpp")
    
    Returns a complete coding question with:
    - Question description
    - Constraints
    - Input/output format
    - Sample input/output
    - Test cases
    """
    try:
        return generate_question(req)
    except ValueError as e:
        error_msg = str(e)
        if "GROQ_API_KEY" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="GROQ_API_KEY is not configured. Please set it in Vercel environment variables.",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_msg
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {e}",
        )
