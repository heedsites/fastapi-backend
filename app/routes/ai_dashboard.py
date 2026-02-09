'''from fastapi import APIRouter
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
    return get_ai_dashboard()'''
from fastapi import APIRouter
from app.models.question_analysis import QuestionAnalysisRequest, QuestionAnalysisResponse
from app.controllers.ai_dashboard import analyze_question_controller
from app.models.batch_insight import BatchInsightRequest
from app.controllers.ai_dashboard import batch_insight_controller
from app.models.query_request import DashboardQueryRequest
from app.controllers.ai_dashboard import query_dashboard_controller


router = APIRouter()


@router.post("/analyze-question", response_model=QuestionAnalysisResponse)
def analyze_question(request: QuestionAnalysisRequest):
    result = analyze_question_controller(request.question)
    return result
from app.models.top_performers import TopPerformersRequest, TopPerformer
from typing import List
from app.controllers.ai_dashboard import top_performers_controller, top_performers_with_summary


@router.post("/top-performers", response_model=List[TopPerformer])
def get_top_performers(request: TopPerformersRequest):
    return top_performers_controller(request.submissions, request.top_n)
@router.post("/top-performers-insight")
def get_top_performers_with_insight(request: TopPerformersRequest):
    return top_performers_with_summary(request.submissions, request.top_n)
@router.post("/batch-insight")
def get_batch_insight(request: BatchInsightRequest):
    return batch_insight_controller(request.submissions)
@router.post("/query")
def dashboard_query(request: DashboardQueryRequest):
    return query_dashboard_controller(request.question, request.submissions)

