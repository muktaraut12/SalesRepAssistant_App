# SalesRepAssistant_App
SalesAssist — AI Powered Product Notes Rewriter A minimal AI chat application built using FastAPI, OpenAI API, and a simple HTML/JS frontend. This project helps Sales &amp; Pre Sales teams convert raw technical product notes into client ready messaging using AI. Demonstrates backend skills, frontend skills, and AI engineering fundamentals.
________________________________________
🚀 Features (MVP)
•	AI-powered rewriting using OpenAI API
•	FastAPI backend with /api/chat endpoint
•	Simple chat interface built with HTML + CSS + JavaScript
•	Tone selection: friendly, concise, technical
•	Optional add-ons: Summary & Email Intro (available in extensions)
•	Error handling & input validation
•	In-memory session context
•	Fully documented API & architecture
________________________________________
🎯 Problem Statement
Sales teams often receive highly technical product updates, but need to quickly translate them into simple, client-friendly summaries.
This tool helps them rewrite notes instantly using AI.
________________________________________
📦 Tech Stack
Backend
•	Python 3.x
•	FastAPI
•	Uvicorn
•	OpenAI API
•	Pydantic
Frontend
•	HTML
•	CSS
•	JavaScript (Fetch API)
________________________________________
🏗️ Architecture
Frontend (HTML/CSS/JS)
        |
        | Fetch API
        ▼
FastAPI Backend ───► /api/chat  → Calls OpenAI → Response
        |
        └── /api/config
•	State: stored on frontend (sessionId), with short in-memory context on backend
•	Security: simple header x-app-secret for development
•	No database: lightweight MVP
________________________________________
📁 Folder Structure
project/
│
├── main.py                   # FastAPI backend
├── requirements.txt
├── .env                      # OpenAI API Key (not committed)
│
└── static/
    ├── index.html
    ├── app.js
    └── styles.css
________________________________________
🛠️ Setup Instructions
1. Clone the repo
git clone <your-repo-url>
cd <repo-name>
2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Add environment variables
Create a .env file in project root:
OPENAI_API_KEY=your_key_here
APP_SECRET=local-dev-key
5. Run the backend
uvicorn main:app --reload
6. Open the frontend
Open:
http://localhost:8000/static/index.html
________________________________________
🔌 API Documentation
POST /api/chat
Request body:
{
  "sessionId": "optional-uuid",
  "tone": "friendly",
  "message": "The product now supports containerized deployments.",
  "addOns": {
    "summary": false,
    "emailIntro": false
  }
}
Response:
{
  "reply": "Here’s a client-friendly explanation...",
  "summary": null,
  "emailIntro": null,
  "usage": {
    "promptTokens": 200,
    "completionTokens": 120,
    "totalTokens": 320
  }
}
GET /api/health
{ "status": "ok" }
``
GET /api/config
{
  "tones": ["friendly", "concise", "technical"],
  "model": "gpt-4o-mini",
  "rateLimitPerSession": 50
}
________________________________________
🖥️ Screenshots
(Add screenshots after UI is complete)
static/screenshots/chat-ui.png
static/screenshots/architecture.png
________________________________________
✨ Roadmap (Future Enhancements)
•	🔹 Streaming responses (typing effect)
•	🔹 JWT authentication
•	🔹 Database for persistent sessions
•	🔹 User accounts + login
•	🔹 Analytics dashboard (token usage, conversations)
•	🔹 Mobile responsive UI
•	🔹 Download conversation as PDF
•	🔹 Advanced roles: Sales, Pre-sales, CSM, Support
•	🔹 Conversation tagging using embeddings
________________________________________
🧪 Testing Checklist
•	OpenAI API key works
•	/api/chat returns proper responses
•	Tone selector affects output
•	Friendly error messages
•	Rate limiting works
•	Frontend handles network failures
________________________________________

## 🏗️ Architecture Diagram

<p align="center">
  docs/architecture.svg
</p>


🧑‍💻 Author
Mukta Raut
Senior Technical Content Developer & AI Engineer
•	Strong in FastAPI, Prompt Engineering, GenAI, and Technical Documentation.
________________________________________
📄 License
MIT License – free to modify and use.
________________________________________
