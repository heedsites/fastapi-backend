from pydantic import BaseModel
from typing import List, Dict


# ---------- BASIC MODELS ----------

class Project(BaseModel):
    title: str
    description: str


class CodingStats(BaseModel):
    problems_solved: int
    topics: List[str]


# ---------- NEW PROFILE MODELS ----------

class Education(BaseModel):
    degree: str
    institution: str
    year: str


class Certification(BaseModel):
    title: str
    provider: str
    year: str


class WorkExperience(BaseModel):
    company: str
    role: str
    description: str


# ---------- REQUEST ----------

class ResumeRequest(BaseModel):
    student_name: str
    target_role: str
    education: str
    skills: List[str]
    projects: List[Project]
    quiz_performance: Dict[str, int]
    coding_stats: CodingStats


# ---------- RESPONSE ----------

class ResumeResponse(BaseModel):
    professional_summary: str
    technical_skills: List[str]
    experience_highlights: List[str]
    project_details: List[str]

    education: List[Education]
    certifications: List[Certification]
    work_experience: List[WorkExperience]
