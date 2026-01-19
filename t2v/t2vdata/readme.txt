# Check Python version (Python 3.9+ recommended)
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install all required dependencies
pip install fastapi uvicorn moviepy gtts python-dotenv groq requests pillow imageio imageio-ffmpeg

# Verify FFmpeg installation
python -c "import imageio_ffmpeg; print('FFmpeg installed successfully')"

# Run the FastAPI application
python -m uvicorn app:app --reload

# Open API docs in browser
# http://127.0.0.1:8000/docs

# Test API using curl
curl -X POST http://127.0.0.1:8000/generate-video \
  -H "Content-Type: application/json" \
  -d '{"text": "Python importance for placement preparation"}'


##############paste this in .env file####################
GROQ_API_KEY=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
HF_API_KEY=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