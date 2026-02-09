# Quick Start Guide

## 🚀 Get Running in 3 Steps

### Step 1: Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Set Up Environment
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Step 3: Run the Server
```bash
uvicorn app.main:app --reload
```

## 📖 Access Swagger Documentation

Once the server is running, open your browser:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/

## 🧪 Quick Test

Test the API using Swagger UI:
1. Go to http://localhost:8000/docs
2. Click on `POST /api/generate-question`
3. Click "Try it out"
4. Use this example:
   ```json
   {
     "topic": "arrays",
     "difficulty": "medium",
     "language": "python"
   }
   ```
5. Click "Execute"

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.
