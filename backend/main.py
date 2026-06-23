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
    modes: list[str]

def detect_signal_type(message: str):

    message = message.lower()

    if "cosine" in message:
        return "cosine"

    elif "sine" in message:
        return "sine"

    elif "square" in message:
        return "square"

    return None


@app.post("/chat")
def chat(request: ChatRequest):
    base_prompt = f"""
You are SignalSense, an AI learning assistant designed specifically for Electronics and Telecommunication Engineering students.

Your goal is to help students understand concepts intuitively.

Rules:
- Explain clearly and simply.
- Use examples whenever possible.
- Avoid markdown formatting.
- Avoid symbols like ## and **.
- Keep responses structured and readable.

User Query:
{request.message}
"""
    modes = request.modes
    prompt_parts = []

    if "notes" in modes:
        prompt_parts.append("""
Generate notes in academic way.

Structure:
1. Definition
2. Formula(s)
3. Conditions
4. Applications
5. Examples
6. Summary

Keep concise and exam-oriented.
""")
        
    if "explanation" in modes:
        prompt_parts.append("""
Explain the concept intuitively.

Rules:
- Start with a real-world analogy.
- Build intuition first.
- Then explain technically.
- Avoid textbook language.
- Make it easy to understand.
""")

    final_prompt = (
    base_prompt
    + "\n\n"
    + "\n".join(prompt_parts)
    )

    signal_type = detect_signal_type(request.message)
    # response = model.generate_content(final_prompt)

    return {
        "response": "Testing 123",
        "signal_type": signal_type
    }