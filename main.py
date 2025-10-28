from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Dynamic FastAPI To-Do & Role Management App")

# ===============================
# 📦 Models
# ===============================
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

# ===============================
# 🧠 In-memory data (temporary database)
# ===============================
roles_db: List[Role] = []
projects_db: List[Project] = []
tasks_db: List[Task] = []

# ===============================
# 🏠 Root
# ===============================
@app.get("/")
def home():
    return {"message": "Welcome to the Dynamic FastAPI To-Do & Role Management App"}

# ===============================
# 👥 Role Management
# ===============================
@app.post("/roles/")
def add_role(role: Role):
    # Check if role already exists
    for existing_role in roles_db:
        if existing_role.id == role.id:
            raise HTTPException(status_code=400, detail="Role ID already exists.")
    roles_db.append(role)
    return {"message": "Role added successfully!", "role": role}

@app.get("/roles/")
def get_roles():
    return {"roles": roles_db}

@app.delete("/roles/{role_id}")
def delete_role(role_id: int):
    for role in roles_db:
        if role.id == role_id:
            roles_db.remove(role)
            return {"message": f"Role ID {role_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Role not found")

# ===============================
# 🧩 Project Management
# ===============================
@app.post("/projects/")
def add_project(project: Project):
    for existing_project in projects_db:
        if existing_project.id == project.id:
            raise HTTPException(status_code=400, detail="Project ID already exists.")
    projects_db.append(project)
    return {"message": "Project created successfully!", "project": project}

@app.get("/projects/")
def get_projects():
    return {"projects": projects_db}

@app.put("/projects/{project_id}")
def update_project(project_id: int, updated_project: Project):
    for i, project in enumerate(projects_db):
        if project.id == project_id:
            projects_db[i] = updated_project
            return {"message": "Project updated successfully!", "project": updated_project}
    raise HTTPException(status_code=404, detail="Project not found")

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    for project in projects_db:
        if project.id == project_id:
            projects_db.remove(project)
            return {"message": f"Project {project_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Project not found")

# ===============================
# ✅ Task Management
# ===============================
@app.post("/tasks/")
def add_task(task: Task):
    for existing_task in tasks_db:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="Task ID already exists.")
    tasks_db.append(task)
    return {"message": "Task added successfully!", "task": task}

@app.get("/tasks/")
def get_tasks():
    return {"tasks": tasks_db}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db[i] = updated_task
            return {"message": "Task updated successfully!", "task": updated_task}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            tasks_db.remove(task)
            return {"message": f"Task {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
