# Vercel entrypoint: export FastAPI app (zero-config FastAPI).
# Local dev: uvicorn app.main:app --reload
from app.main import app

__all__ = ["app"]
