# Vercel Deployment Setup Guide

## 🔧 Fixing `TypeError: issubclass() arg 1 must be a class` (FUNCTION_INVOCATION_FAILED)

This error happens when using **custom builds** (`@vercel/python`) with **Mangum**. Vercel’s legacy Python handler expects a WSGI app or `BaseHTTPRequestHandler`; Mangum is an ASGI adapter, so the internal `issubclass(...)` check fails.

**Fix**: Use **Vercel’s native FastAPI support** (zero config). No Mangum, no custom builds.

**What we use**:
- **Entrypoint**: `app.py` at project root exports the FastAPI `app` (from `app.main`).
- **vercel.json**: No `builds` or `routes`. Only `version` and optional `env` (e.g. `PYTHONPATH`).
- **No** `api/index.py`, **no** Mangum, **no** `@vercel/python` build.

Vercel auto-detects FastAPI and runs `app` from `app.py`.

## 🔧 Fixing the 500 Error (Missing API Key)

The 500 error is often due to missing environment variables.

### Step 1: Add Environment Variables in Vercel

1. Go to your Vercel project dashboard.
2. Open **Settings** → **Environment Variables**.
3. Add:
   - **Name**: `GROQ_API_KEY`
   - **Value**: Your Groq API key (from https://console.groq.com/)
   - **Environment**: Production, Preview, Development (select all)
4. Click **Save**.

### Step 2: Redeploy

1. Go to the **Deployments** tab.
2. Click **⋯** on the latest deployment → **Redeploy**.
3. Uncheck **Use existing Build Cache**.

### Step 3: Verify

- Root: `https://your-app.vercel.app/`
- Docs: `https://your-app.vercel.app/docs`

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"

Add `GROQ_API_KEY` in Vercel environment variables and redeploy.

### FUNCTION_INVOCATION_FAILED

1. **`issubclass() arg 1 must be a class`**  
   Use native FastAPI (`app.py`, no Mangum, no custom builds) as above.

2. **Other causes**  
   - Missing env vars (e.g. `GROQ_API_KEY`).  
   - Import errors → check **Build** and **Function** logs.  
   - Missing deps → ensure `requirements.txt` includes everything.

**Check logs**: Vercel Dashboard → Project → Deployments → deployment → **Function Logs**.

### Module not found

List all dependencies in `requirements.txt`, e.g.:

```
fastapi
uvicorn
groq
python-dotenv
```

**Do not** add the standalone `typing` package; it can break FastAPI/Pydantic on Vercel.

## 📝 Environment Variables Checklist

- [ ] `GROQ_API_KEY` – required for coding questions and chatbot

## 🔍 Testing Locally Before Deploying

1. Create a `.env` in the project root:

   ```env
   GROQ_API_KEY=your_key_here
   ```

2. Run:

   ```bash
   uvicorn app.main:app --reload
   ```

3. Test:
   - `http://localhost:8000/` – health (no API key)
   - `http://localhost:8000/api/generate-question` – needs API key

## ✅ Success Indicators

- `/` returns JSON with API info.
- `/docs` loads Swagger UI.
- `/api/generate-question` works when `GROQ_API_KEY` is set, or returns a clear error when not.
