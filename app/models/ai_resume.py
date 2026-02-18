from pydantic import BaseModel
from typing import List, Dict


class Project(BaseModel):
    title: str
    description: str


class CodingStats(BaseModel):
    problems_solved: int
    topics: List[str]


class ResumeRequest(BaseModel):
    student_name: str
    target_role: str
    education: str
    skills: List[str]
    projects: List[Project]
    quiz_performance: Dict[str, int]
    coding_stats: CodingStats


class ResumeResponse(BaseModel):
    professional_summary: str
    technical_skills: List[str]
    experience_highlights: List[str]
    project_details: List[str]

