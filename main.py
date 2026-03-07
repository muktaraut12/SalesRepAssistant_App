import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

# Load environment variables from .env (if present)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create FastAPI app
app = FastAPI(title="Sales Rep Assistant")

# Serve static frontend (index.html, app.js, styles.css) from /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Allow browser frontend to call backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # MVP: allow all; restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Request model (use snake_case for Python / FastAPI) ----
class ChatRequest(BaseModel):
    session_id: str | None = None
    tone: str
    message: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/config")
def config():
    return {
        "tones": ["friendly", "concise", "technical"],
        "model": "gpt-4o-mini"
    }


@app.post("/api/chat")
def chat(req: ChatRequest):
    # Basic validations
    if not OPENAI_API_KEY:
        raise HTTPException(500, "Missing OpenAI API Key in environment")
    if req.tone not in ["friendly", "concise", "technical"]:
        raise HTTPException(400, "Invalid tone")

    # Strong system prompt to force rewriting (no echo)
    system_prompt = """
You are SalesAssist AI. Rewrite raw technical product notes into clear, client-friendly language.
Rules:
- Do NOT repeat the user's text verbatim.
- Always rewrite, simplify, reorganize for clarity.
- Follow the selected tone strictly.
- Keep it accurate and professional.
"""

    try:
        # Call OpenAI
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""
REWRITE the following product notes using a {req.tone} tone.
Do NOT repeat the text word-for-word. Transform wording and structure while preserving meaning.

TEXT:
{req.message}
"""
                }
            ],
            temperature=0.7
        )

        ai_reply = resp.choices[0].message.content

        # Optional: token usage if available
        # usage_info = getattr(resp, "usage", None)
        # print("Token usage:", usage_info)

        # Return camelCase to the frontend (convention for JSON/JS)
        return {
            "reply": ai_reply,
            "sessionId": req.session_id or "new-session"
        }

    except Exception as e:
        # Log the exact error for debugging
        print("OpenAI error:", repr(e))
        raise HTTPException(500, "AI request failed")