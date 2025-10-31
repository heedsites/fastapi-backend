import os
from groq import Groq

class GroqChatbot:   
    def __init__(self, api_key, model="llama3-8b-8192"):
        self.model = model
        self.api_key = api_key
        self.client = self._get_client()
        self.system_prompt = self._initialize_system_prompt()
        
        print(f"--- Groq Chatbot Client Initialized (Model: {self.model}) ---")
    def _get_client(self):
        try:
            client = Groq(api_key=self.api_key)
            client.chat.completions.create(messages=[{"role": "user", "content": "test"}], model="llama-3.1-8b-instant", max_tokens=10)
            print("Groq client initialized and key validated.")
            return client
        except Exception as e:
            print(f"Failed to initialize Groq client: {e}")
            return None

    def _initialize_system_prompt(self):
        return {
            "role": "system",
            "content": "AI assistant."
        }

    def get_response(self, user_input):
        messages_to_send = [
            self.system_prompt,
            {"role": "user", "content": user_input}
        ]

        chat_completion = self.client.chat.completions.create(
            messages=messages_to_send,
            model=self.model,
            temperature=0.7,
            stream=False
        )
            
        return chat_completion.choices[0].message.content
