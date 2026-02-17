from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from app.routes import groq_chatbot_router, coding_questions_router
from app.routes.ai_dashboard import router as ai_dashboard_router
from app.routes.ai_resume import router as ai_resume_router


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
app.include_router(ai_dashboard_router, prefix="/api", tags=["AI Dashboard"])
app.include_router(groq_chatbot_router, prefix="/api", tags=["Groq Chatbot"])
app.include_router(coding_questions_router, prefix="/api", tags=["Coding Questions"])
app.include_router(ai_resume_router)

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint - API health check.
    """
    return {
        "message": "Hello from Heedsites backend – live!",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }
