# Routes (API layer)
from app.routes.ai_dashboard import router as ai_dashboard_router
from app.routes.groq_chatbot import router as groq_chatbot_router
from app.routes.coding_questions import router as coding_questions_router

__all__ = ["ai_dashboard_router", "groq_chatbot_router", "coding_questions_router"]
