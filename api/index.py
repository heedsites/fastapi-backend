# api/index.py
import sys
import os
from pathlib import Path

# Add parent directory to Python path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# Set environment to production if not set
os.environ.setdefault('ENV', 'production')

# Now import the app
try:
    from app.main import app
    print("✓ Successfully imported app from app.main")
except ImportError as e:
    print(f"✗ Failed to import app: {e}")
    # Create a fallback app for debugging
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    def error_root():
        return {
            "error": "Failed to import main app",
            "details": str(e),
            "sys_path": sys.path[:3]
        }

# Wrap with Mangum for Vercel
from mangum import Mangum
handler = Mangum(app, lifespan="off")
