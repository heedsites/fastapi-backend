# Heedsites FastAPI Backend

A FastAPI backend application with AI Dashboard, Groq Chatbot, and Coding Questions Generator.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)

## ✨ Features

- **AI Dashboard** - Dashboard endpoint for AI features
- **Groq Chatbot** - Integration with Groq AI chatbot
- **Coding Questions Generator** - AI-powered coding question generator
- **Swagger/OpenAPI Documentation** - Interactive API documentation
- **CORS Support** - Cross-origin resource sharing enabled

## 📁 Project Structure

```
fastapi-backend/
├── api/
│   └── index.py              # Vercel serverless entry point
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI application setup
│   ├── models/               # Pydantic models (schemas)
│   │   ├── __init__.py
│   │   └── coding_questions.py
│   ├── controllers/          # Business logic
│   │   ├── __init__.py
│   │   ├── ai_dashboard.py
│   │   ├── groq_chatbot.py
│   │   └── coding_questions.py
│   └── routes/               # API routes (endpoints)
│       ├── __init__.py
│       ├── ai_dashboard.py
│       ├── groq_chatbot.py
│       └── coding_questions.py
├── index.py                  # Vercel entrypoint (exports FastAPI app)
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel deployment configuration
└── README.md                # This file
```

## 🔧 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Groq API key (for coding questions generator)

## 📦 Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd fastapi-backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Create a `.env` file** in the root directory:
   ```bash
   touch .env
   ```

2. **Add your Groq API key** to the `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

   > **Note**: Get your Groq API key from [https://console.groq.com/](https://console.groq.com/)

## 🚀 Running the Application

### Local Development

1. **Make sure your virtual environment is activated** (see Installation step 3)

2. **Run the application** using uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```
   
   Or using the convenience script:
   ```bash
   uvicorn app:app --reload
   ```

3. **The API will be available at**:
   - API: `http://localhost:8000`
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`
   - OpenAPI JSON: `http://localhost:8000/openapi.json`

### Running on a Different Port

```bash
uvicorn app.main:app --reload --port 8080
```

### Running in Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

FastAPI automatically generates interactive API documentation:

### Swagger UI
Visit **`http://localhost:8000/docs`** for interactive Swagger documentation where you can:
- View all available endpoints
- See request/response schemas
- Test API endpoints directly in the browser
- View example requests and responses

### ReDoc
Visit **`http://localhost:8000/redoc`** for alternative ReDoc documentation with a clean, readable format.

### OpenAPI Schema
Visit **`http://localhost:8000/openapi.json`** to get the raw OpenAPI JSON schema.

## 🔌 API Endpoints

### Root
- **GET** `/` - Health check and API information

### AI Dashboard
- **GET** `/api/ai-dashboard` - Get AI Dashboard information

### Groq Chatbot
- **GET** `/api/groq-chatbot` - Get Groq Chatbot information

### Coding Questions
- **POST** `/api/generate-question` - Generate a coding question
  - **Request Body**:
    ```json
    {
      "topic": "arrays",
      "difficulty": "medium",
      "language": "python"
    }
    ```
  - **Response**:
    ```json
    {
      "question": "Find the sum of all elements...",
      "constraints": "1 <= n <= 1000",
      "input_format": "First line contains n...",
      "output_format": "Print a single integer...",
      "sample_input": "5\n1 2 3 4 5",
      "sample_output": "15",
      "test_cases": [
        {
          "input": "5\n1 2 3 4 5",
          "output": "15"
        }
      ]
    }
    ```

## 🧪 Testing the API

### Using Swagger UI
1. Open `http://localhost:8000/docs`
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the request body (if needed)
5. Click "Execute"
6. View the response

### Using cURL

**Health Check**:
```bash
curl http://localhost:8000/
```

**Generate Coding Question**:
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

# Generate a coding question
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

## 🚢 Deployment

### Vercel Deployment

This project is configured for Vercel deployment:

1. **Push your code to GitHub**

2. **Connect your repository to Vercel**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will automatically detect the FastAPI configuration

3. **Add Environment Variables**:
   - In Vercel project settings, add `GROQ_API_KEY`
   - Set the value to your Groq API key

4. **Deploy**:
   - Vercel will automatically deploy on every push to main branch
   - Or click "Deploy" to deploy manually

### Manual Deployment

For other platforms (AWS, GCP, Azure, etc.), use:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🛠️ Development

### Project Architecture

- **Models** (`app/models/`): Pydantic schemas for request/response validation
- **Controllers** (`app/controllers/`): Business logic and external API calls
- **Routes** (`app/routes/`): API endpoint definitions that wire to controllers
- **Main** (`app/main.py`): FastAPI app initialization and route registration

### Adding a New Endpoint

1. **Create a model** in `app/models/` (if needed)
2. **Create a controller** in `app/controllers/` with business logic
3. **Create a route** in `app/routes/` that uses the controller
4. **Register the route** in `app/main.py`

## 📝 License

This project is part of Heedsites backend services.

## 🤝 Support

For issues and questions, please open an issue in the repository.
