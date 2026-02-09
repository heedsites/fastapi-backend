from fastapi import APIRouter
from app.controllers.ai_dashboard import get_ai_dashboard

router = APIRouter(tags=["AI Dashboard"])


@router.get(
    "/ai-dashboard",
    summary="Get AI Dashboard",
    description="Returns AI Dashboard information and status",
    response_description="AI Dashboard data",
)
def ai_dashboard():
    """
    Get AI Dashboard endpoint.
    
    Returns dashboard information and status for the AI features.
    """
    return get_ai_dashboard()
