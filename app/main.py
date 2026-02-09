from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from app.routes import groq_chatbot_router, coding_questions_router
from app.routes.ai_dashboard import router as ai_dashboard_router
app = FastAPI(
    title="Heedsites Backend API",
    description="FastAPI backend with AI Dashboard, Groq Chatbot, and Coding Questions Generator",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules

app.include_router(ai_dashboard_router, prefix="/ai-dashboard", tags=["AI Dashboard"])
app.include_router(groq_chatbot_router, prefix="/api", tags=["Groq Chatbot"])
app.include_router(coding_questions_router, prefix="/api", tags=["Coding Questions"])


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint - API health check.
    
    Returns a welcome message confirming the API is running.
    """
    return {
        "message": "Hello from Heedsites backend – live!",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }



