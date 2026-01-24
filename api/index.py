from mangum import Mangum
from app.main import app

# Vercel serverless function entry point
# Wrap FastAPI app with Mangum ASGI adapter for Vercel
handler = Mangum(app, lifespan="off")
