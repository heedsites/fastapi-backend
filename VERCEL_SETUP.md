# Vercel Deployment Setup Guide

## 🔧 Fixing the 500 Error / TypeError

### Common Error: `TypeError: issubclass() arg 1 must be a class`

This error occurs when Vercel can't properly handle the FastAPI app. The solution is to use **Mangum** as an ASGI adapter.

**Solution Applied**:
- Added `mangum` to `requirements.txt`
- Updated `api/index.py` to wrap FastAPI app with Mangum

If you still see this error after deploying:
1. Make sure `mangum` is in `requirements.txt`
2. Verify `api/index.py` uses: `handler = Mangum(app, lifespan="off")`
3. Redeploy without build cache

## 🔧 Fixing the 500 Error (Missing API Key)

The 500 error is likely due to missing environment variables. Follow these steps:

### Step 1: Add Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add the following environment variable:

   **Name**: `GROQ_API_KEY`  
   **Value**: Your Groq API key (get it from https://console.groq.com/)  
   **Environment**: Production, Preview, Development (select all)

4. Click **Save**

### Step 2: Redeploy

After adding the environment variable:

1. Go to **Deployments** tab
2. Click the **⋯** (three dots) on the latest deployment
3. Click **Redeploy**
4. Make sure to check **"Use existing Build Cache"** is unchecked (to ensure new env vars are picked up)

### Step 3: Verify

1. Visit your deployed URL
2. Check the root endpoint: `https://your-app.vercel.app/`
3. Check Swagger docs: `https://your-app.vercel.app/docs`

## 🐛 Troubleshooting

### Error: "GROQ_API_KEY not found"

**Solution**: Make sure you've added `GROQ_API_KEY` in Vercel environment variables and redeployed.

### Error: "FUNCTION_INVOCATION_FAILED"

**Possible causes**:
1. Missing environment variable (see above)
2. Import error - check Vercel build logs
3. Missing dependency - ensure `requirements.txt` has all packages

**Check logs**:
1. Go to Vercel Dashboard → Your Project → Deployments
2. Click on the failed deployment
3. Check the **Function Logs** tab for detailed error messages

### Error: Module not found

**Solution**: Ensure all dependencies are in `requirements.txt`:
```
fastapi
uvicorn
groq
python-dotenv
```

## 📝 Environment Variables Checklist

- [ ] `GROQ_API_KEY` - Required for coding questions and chatbot features

## 🔍 Testing Locally Before Deploying

1. Create a `.env` file in the root:
   ```env
   GROQ_API_KEY=your_key_here
   ```

2. Run locally:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Test endpoints:
   - `http://localhost:8000/` - Should work (no API key needed)
   - `http://localhost:8000/api/generate-question` - Needs API key

## ✅ Success Indicators

When everything is working:
- Root endpoint (`/`) returns JSON with API info
- Swagger docs (`/docs`) loads correctly
- `/api/generate-question` returns questions (if API key is set) or a clear error message (if not set)
