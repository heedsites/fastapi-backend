from fastapi import APIRouter
from typing import List

from app.controllers.ai_dashboard import (
    analyze_question_controller,
    top_performers_controller,
    top_performers_with_summary,
    batch_insight_controller,
    query_dashboard_controller,
)

from app.models.question_analysis import QuestionAnalysisRequest, QuestionAnalysisResponse
from app.models.top_performers import TopPerformersRequest, TopPerformer
from app.models.batch_insight import BatchInsightRequest
from app.models.query_request import DashboardQueryRequest

router = APIRouter(tags=["AI Dashboard"])


@router.post("/analyze-question", response_model=QuestionAnalysisResponse)
def analyze_question(request: QuestionAnalysisRequest):
    return analyze_question_controller(request.question)


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
