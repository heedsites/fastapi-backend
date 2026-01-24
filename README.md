# Heedsites FastAPI Backend

A modern, production-ready FastAPI backend application with AI Dashboard, Groq Chatbot integration, and an AI-powered Coding Questions Generator. Deployed on Vercel with zero-configuration FastAPI support.

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [API Endpoints](#-api-endpoints)
- [Testing the API](#-testing-the-api)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)

## ✨ Features

- **AI Dashboard** - Dashboard endpoint for AI features and status
- **Groq Chatbot** - Integration with Groq AI chatbot services
- **Coding Questions Generator** - AI-powered coding question generator using Groq's LLM
- **Interactive API Documentation** - Swagger UI and ReDoc for testing and exploration
- **CORS Support** - Cross-origin resource sharing enabled for frontend integration
- **Type Safety** - Pydantic models for request/response validation
- **Zero-Config Deployment** - Native Vercel FastAPI support (no Mangum, no custom builds)

## 📁 Project Structure

```
fastapi-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application setup and configuration
│   ├── models/                    # Pydantic models (request/response schemas)
│   │   ├── __init__.py
│   │   └── coding_questions.py   # QuestionRequest, QuestionResponse, TestCase models
│   ├── controllers/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── ai_dashboard.py        # AI Dashboard controller
│   │   ├── groq_chatbot.py        # Groq Chatbot controller
│   │   └── coding_questions.py    # Coding questions generation logic
│   └── routes/                    # API routes (endpoints)
│       ├── __init__.py
│       ├── ai_dashboard.py        # AI Dashboard routes
│       ├── groq_chatbot.py        # Groq Chatbot routes
│       └── coding_questions.py    # Coding questions routes
├── index.py                       # Vercel entrypoint (exports FastAPI app)
├── requirements.txt               # Python dependencies
├── vercel.json                    # Vercel deployment configuration
├── VERCEL_SETUP.md               # Detailed Vercel deployment guide
├── FUNCTION_INVOCATION_FAILED_FIX.md  # Error troubleshooting guide
└── README.md                      # This file
```

### Architecture Overview

- **Models** (`app/models/`): Pydantic schemas for request/response validation and type safety
- **Controllers** (`app/controllers/`): Business logic, external API calls (Groq), and data processing
- **Routes** (`app/routes/`): API endpoint definitions that wire controllers to HTTP methods
- **Main** (`app/main.py`): FastAPI app initialization, middleware setup, and route registration
- **Entrypoint** (`index.py`): Vercel serverless function entry point (zero-config FastAPI)

## 🔧 Prerequisites

- **Python 3.8+** (Python 3.9+ recommended)
- **pip** (Python package manager)
- **Groq API Key** (for coding questions generator and chatbot features)
  - Get your API key from [Groq Console](https://console.groq.com/)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fastapi-backend
```

### 2. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `fastapi==0.104.1` - Modern web framework
- `uvicorn==0.24.0` - ASGI server
- `pydantic==2.5.0` - Data validation
- `groq==0.11.0` - Groq AI SDK
- `python-dotenv==1.0.0` - Environment variable management

## ⚙️ Configuration

### Environment Variables

1. **Create a `.env` file** in the root directory:
   ```bash
   touch .env
   ```

2. **Add your Groq API key**:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

   > **Note**: Get your Groq API key from [https://console.groq.com/](https://console.groq.com/)

3. **Optional**: Add other environment variables:
   ```env
   ENV=development
   ```

## 🚀 Running the Application

### Local Development

1. **Activate your virtual environment** (if not already active):
   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate      # Windows
   ```

2. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

   The `--reload` flag enables auto-reload on code changes.

3. **Access the API**:
   - **API Base URL**: `http://localhost:8000`
   - **Swagger UI**: `http://localhost:8000/docs`
   - **ReDoc**: `http://localhost:8000/redoc`
   - **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### Running on Different Port

```bash
uvicorn app.main:app --reload --port 8080
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

FastAPI automatically generates interactive API documentation using OpenAPI 3.0.

### Swagger UI

**URL**: `http://localhost:8000/docs` (local) or `https://your-app.vercel.app/docs` (production)

**Features:**
- View all available endpoints
- See request/response schemas with examples
- Test API endpoints directly in the browser
- View example requests and responses
- See response status codes and error formats

### ReDoc

**URL**: `http://localhost:8000/redoc` (local) or `https://your-app.vercel.app/redoc` (production)

**Features:**
- Clean, readable documentation format
- Three-panel layout for easy navigation
- Search functionality
- Print-friendly format

### OpenAPI Schema

**URL**: `http://localhost:8000/openapi.json` (local) or `https://your-app.vercel.app/openapi.json` (production)

Returns the raw OpenAPI 3.0 JSON schema that can be imported into API testing tools like Postman, Insomnia, or used for code generation.

## 🔌 API Endpoints

### Base URL

- **Local**: `http://localhost:8000`
- **Production**: `https://your-app.vercel.app`

All API endpoints are prefixed with `/api` except the root endpoint.

---

### 1. Root Endpoint

**GET** `/`

Health check and API information endpoint.

**Response:**
```json
{
  "message": "Hello from Heedsites backend – live!",
  "docs": "/docs",
  "redoc": "/redoc",
  "openapi": "/openapi.json"
}
```

**Status Codes:**
- `200 OK` - API is running

**Example:**
```bash
curl http://localhost:8000/
```

---

### 2. AI Dashboard

**GET** `/api/ai-dashboard`

Get AI Dashboard information and status.

**Response:**
```json
{
  "message": "AI Dashboard endpoint"
}
```

**Status Codes:**
- `200 OK` - Success

**Example:**
```bash
curl http://localhost:8000/api/ai-dashboard
```

---

### 3. Groq Chatbot

**GET** `/api/groq-chatbot`

Get Groq Chatbot information and status.

**Response:**
```json
{
  "message": "Groq Chatbot endpoint"
}
```

**Status Codes:**
- `200 OK` - Success

**Example:**
```bash
curl http://localhost:8000/api/groq-chatbot
```

---

### 4. Generate Coding Question

**POST** `/api/generate-question`

Generate a coding question using AI based on topic, difficulty, and programming language.

**Request Body:**
```json
{
  "topic": "arrays",
  "difficulty": "medium",
  "language": "python"
}
```

**Request Schema:**
- `topic` (string, required): The topic/subject of the coding question
  - Examples: `"arrays"`, `"sorting"`, `"trees"`, `"dynamic programming"`
- `difficulty` (string, required): Difficulty level
  - Examples: `"easy"`, `"medium"`, `"hard"`
- `language` (string, required): Programming language
  - Examples: `"python"`, `"java"`, `"cpp"`, `"javascript"`

**Response:**
```json
{
  "question": "Find the sum of all elements in an array",
  "constraints": "1 <= n <= 1000, -1000 <= arr[i] <= 1000",
  "input_format": "First line contains n, second line contains n space-separated integers",
  "output_format": "Print a single integer representing the sum",
  "sample_input": "5\n1 2 3 4 5",
  "sample_output": "15",
  "test_cases": [
    {
      "input": "5\n1 2 3 4 5",
      "output": "15"
    },
    {
      "input": "3\n10 20 30",
      "output": "60"
    }
  ]
}
```

**Response Schema:**
- `question` (string): The coding question description
- `constraints` (string): Constraints for the problem
- `input_format` (string): Format specification for input
- `output_format` (string): Format specification for output
- `sample_input` (string): Sample input example
- `sample_output` (string): Sample output example
- `test_cases` (array): List of test cases with input/output pairs
  - Each test case has `input` and `output` fields

**Status Codes:**
- `200 OK` - Successfully generated coding question
- `500 Internal Server Error` - Server error or failed to generate question
- `503 Service Unavailable` - GROQ_API_KEY not configured

**Error Responses:**

**503 Service Unavailable** (API key missing):
```json
{
  "detail": "GROQ_API_KEY is not configured. Please set it in Vercel environment variables."
}
```

**500 Internal Server Error** (Generation failed):
```json
{
  "detail": "Groq API request failed: [error details]"
}
```

**Example Requests:**

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/generate-question" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "arrays",
    "difficulty": "medium",
    "language": "python"
  }'
```

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/generate-question",
    json={
        "topic": "arrays",
        "difficulty": "medium",
        "language": "python"
    }
)
print(response.json())
```

**JavaScript (fetch):**
```javascript
fetch('http://localhost:8000/api/generate-question', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    topic: 'arrays',
    difficulty: 'medium',
    language: 'python'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 🧪 Testing the API

### Using Swagger UI (Recommended)

1. Open `http://localhost:8000/docs` in your browser
2. Click on any endpoint to expand it
3. Click **"Try it out"**
4. Fill in the request body (if needed)
5. Click **"Execute"**
6. View the response in the **"Responses"** section

### Using cURL

**Health Check:**
```bash
curl http://localhost:8000/
```

**AI Dashboard:**
```bash
curl http://localhost:8000/api/ai-dashboard
```

**Groq Chatbot:**
```bash
curl http://localhost:8000/api/groq-chatbot
```

**Generate Coding Question:**
```bash
curl -X POST "http://localhost:8000/api/generate-question" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "arrays",
    "difficulty": "medium",
    "language": "python"
  }'
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/")
print(response.json())

# Generate coding question
response = requests.post(
    f"{BASE_URL}/api/generate-question",
    json={
        "topic": "arrays",
        "difficulty": "medium",
        "language": "python"
    }
)
print(response.json())
```

### Using Postman/Insomnia

1. Import the OpenAPI schema from `http://localhost:8000/openapi.json`
2. All endpoints will be automatically configured
3. Test each endpoint with different request bodies

## 🚢 Deployment

### Vercel Deployment (Recommended)

This project uses **Vercel's native FastAPI support** (zero-configuration). No Mangum, no custom builds required.

#### Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Groq API Key**: Get it from [console.groq.com](https://console.groq.com/)

#### Deployment Steps

1. **Connect Repository to Vercel**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click **"New Project"**
   - Import your GitHub repository
   - Vercel will automatically detect FastAPI configuration

2. **Add Environment Variables**:
   - In Vercel project settings, go to **Settings** → **Environment Variables**
   - Add `GROQ_API_KEY` with your Groq API key
   - Select all environments (Production, Preview, Development)
   - Click **Save**

3. **Deploy**:
   - Vercel will automatically deploy on every push to the main branch
   - Or click **"Deploy"** to deploy manually
   - Wait for deployment to complete

4. **Verify Deployment**:
   - Visit your deployment URL: `https://your-app.vercel.app`
   - Check Swagger docs: `https://your-app.vercel.app/docs`
   - Test the root endpoint: `https://your-app.vercel.app/`

#### Project Configuration

**vercel.json** (already configured):
```json
{
  "version": 2,
  "env": {
    "PYTHONPATH": "."
  }
}
```

**Entrypoint**: `index.py` exports the FastAPI app from `app.main`

**Important Notes:**
- ✅ Uses native FastAPI support (no Mangum, no `@vercel/python` builds)
- ✅ Entrypoint is `index.py` (not `app.py` to avoid import conflicts)
- ✅ All routes are automatically detected and served

#### Environment Variables in Vercel

Required:
- `GROQ_API_KEY` - Your Groq API key for AI features

Optional:
- `ENV` - Environment name (defaults to "production")

### Manual Deployment (Other Platforms)

For AWS, GCP, Azure, Docker, etc.:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Docker Example:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🐛 Troubleshooting

### Common Issues

#### 1. `ModuleNotFoundError: No module named 'app.main'`

**Cause**: Python import conflict - having both `app.py` (file) and `app/` (directory).

**Solution**: Use `index.py` as the entrypoint (already configured). Never use `app.py` when you have an `app/` directory.

#### 2. `FUNCTION_INVOCATION_FAILED` / `TypeError: issubclass() arg 1 must be a class`

**Cause**: Using custom builds (`@vercel/python`) with Mangum adapter.

**Solution**: Use Vercel's native FastAPI support (zero-config). See `VERCEL_SETUP.md` for details.

#### 3. `503 Service Unavailable` - GROQ_API_KEY not configured

**Cause**: Missing `GROQ_API_KEY` environment variable.

**Solution**:
- **Local**: Add `GROQ_API_KEY=your_key` to `.env` file
- **Vercel**: Add `GROQ_API_KEY` in Vercel project settings → Environment Variables

#### 4. `500 Internal Server Error` - Groq API request failed

**Possible Causes**:
- Invalid Groq API key
- Groq API rate limit exceeded
- Network connectivity issues
- Invalid request format

**Solution**: Check Vercel Function Logs for detailed error messages.

#### 5. Import Errors

**Cause**: Missing dependencies or incorrect Python path.

**Solution**:
- Ensure all packages are in `requirements.txt`
- Check `PYTHONPATH` in `vercel.json`
- Verify virtual environment is activated locally

### Debugging Tips

1. **Check Vercel Logs**:
   - Go to Vercel Dashboard → Your Project → Deployments
   - Click on the deployment → **Function Logs**
   - Look for error messages and stack traces

2. **Test Locally First**:
   - Always test endpoints locally before deploying
   - Use `uvicorn app.main:app --reload` for development

3. **Verify Environment Variables**:
   - Check `.env` file exists locally
   - Verify environment variables in Vercel dashboard
   - Redeploy after adding/changing environment variables

4. **Check API Documentation**:
   - Visit `/docs` to see all available endpoints
   - Test endpoints directly in Swagger UI

For more detailed troubleshooting, see:
- `VERCEL_SETUP.md` - Vercel-specific deployment guide
- `FUNCTION_INVOCATION_FAILED_FIX.md` - Error resolution guide

## 🛠️ Development

### Project Architecture

**MVC-like Structure:**
- **Models** (`app/models/`): Data schemas and validation (Pydantic)
- **Controllers** (`app/controllers/`): Business logic and external API integration
- **Routes** (`app/routes/`): HTTP endpoint definitions
- **Main** (`app/main.py`): Application setup and configuration

### Adding a New Endpoint

1. **Create a Model** (if needed) in `app/models/`:
   ```python
   from pydantic import BaseModel, Field
   
   class MyRequest(BaseModel):
       field: str = Field(..., description="Field description")
   ```

2. **Create a Controller** in `app/controllers/`:
   ```python
   def my_controller(req: MyRequest):
       # Business logic here
       return {"result": "data"}
   ```

3. **Create a Route** in `app/routes/`:
   ```python
   from fastapi import APIRouter
   from app.controllers.my_controller import my_controller
   from app.models.my_model import MyRequest
   
   router = APIRouter(tags=["My Feature"])
   
   @router.post("/my-endpoint")
   def my_endpoint(req: MyRequest):
       return my_controller(req)
   ```

4. **Register the Route** in `app/main.py`:
   ```python
   from app.routes.my_routes import router as my_router
   
   app.include_router(my_router, prefix="/api", tags=["My Feature"])
   ```

### Code Style

- Follow PEP 8 Python style guide
- Use type hints for all function parameters and return types
- Add docstrings to all functions and classes
- Use Pydantic models for request/response validation

### Testing

```bash
# Run tests (if you add them)
pytest

# Run with coverage
pytest --cov=app
```

## 📝 License

This project is part of Heedsites backend services.

## 🤝 Support

For issues, questions, or contributions:
- Open an issue in the repository
- Check `VERCEL_SETUP.md` for deployment help
- Review `FUNCTION_INVOCATION_FAILED_FIX.md` for error troubleshooting

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vercel FastAPI Guide](https://vercel.com/docs/frameworks/backend/fastapi)
- [Groq API Documentation](https://console.groq.com/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAPI Specification](https://swagger.io/specification/)

---

**Built with ❤️ using FastAPI and deployed on Vercel**
