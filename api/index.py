# api/index.py
"""
Vercel serverless function entry point for FastAPI application.

This file serves as the bridge between Vercel's serverless runtime
and the FastAPI ASGI application using Mangum adapter.
"""
import sys
import os
from pathlib import Path

# Add parent directory to Python path for imports
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# Set environment to production if not set
os.environ.setdefault('ENV', 'production')

# Import the FastAPI app
# If this fails, let it fail loudly - don't mask the error
from app.main import app

# Wrap FastAPI app with Mangum for Vercel's serverless environment
# Mangum converts ASGI (FastAPI) to AWS Lambda/API Gateway format
from mangum import Mangum

# Create the handler - this is what Vercel will invoke
# lifespan="off" disables FastAPI lifespan events (startup/shutdown)
# which don't work well in serverless environments
handler = Mangum(app, lifespan="off")
