from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware   

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    prompt = f"""
You are SignalSense, an AI learning assistant designed specifically for Electronics and Telecommunication Engineering students.

Your goal is to help students understand concepts intuitively.

Rules:
- Explain clearly and simply.
- Use examples whenever possible.
- Avoid markdown formatting.
- Avoid symbols like ## and **.
- Keep responses structured and readable.
- If the user asks for notes, provide detailed academic style notes.
- If the user asks for explanation, explain in depth.

User Query:
{request.message}
"""
    response = model.generate_content(prompt)

    return {
        "response": response.text
    }