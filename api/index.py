# api/index.py
import sys
from pathlib import Path

# Add the parent directory to Python path so we can import from 'app' package
# This allows: from app.main import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from mangum import Mangum
from app.main import app

# Vercel serverless function entry point
handler = Mangum(app, lifespan="off")