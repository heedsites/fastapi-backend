from fastapi import APIRouter
from app.controllers.groq_chatbot import get_groq_chatbot

router = APIRouter(tags=["Groq Chatbot"])


@router.get(
    "/groq-chatbot",
    summary="Get Groq Chatbot",
    description="Returns Groq Chatbot information and status",
    response_description="Groq Chatbot data",
)
def groq_chatbot():
    """
    Get Groq Chatbot endpoint.
    
    Returns chatbot information and status for Groq integration.
    """
    return get_groq_chatbot()
