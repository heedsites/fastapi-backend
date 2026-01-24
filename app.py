from fastapi import FastAPI
from app.api import ai_dashboard, groq_chatbot

# Create FastAPI instance
app = FastAPI(title="Heedsites Backend", version="1.0.0")

# Include routers from your API modules
app.include_router(ai_dashboard.router, prefix="/api", tags=["AI Dashboard"])
app.include_router(groq_chatbot.router, prefix="/api", tags=["Groq Chatbot"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Hello from root app.py - Heedsites backend is live!"}
 