# Import app from the app package for local development convenience
# For Vercel deployment, use api/index.py as the entry point
from app.main import app

# Re-export app for uvicorn and local development
__all__ = ["app"]
 