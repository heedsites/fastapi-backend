from fastapi import FastAPI
from pydantic import BaseModel
from groq_chatbot import GroqChatbot 

app = FastAPI()

GROQ_API_KEY = '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' 


chatbot = GroqChatbot(api_key='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', model="llama-3.1-8b-instant")

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):


    bot_response = chatbot.get_response(request.prompt)
    
    return {"response": bot_response}

@app.get("/")
async def root():
    return {"ABCD"}
