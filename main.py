from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from ai_dashboard import router as ai_dashboard_router

app = FastAPI(title="Dynamic FastAPI To-Do & Role Management App")

class Role(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    roles: List[str] = []

class Task(BaseModel):
    id: int
    name: str
    assigned_to: Optional[str] = None
    status: str = "Pending"

roles_db: List[Role] = []
projects_db: List[Project] = []
tasks_db: List[Task] = []

@app.get("/")
def home():
    return {"message": "API running successfully"}

app.include_router(ai_dashboard_router)
