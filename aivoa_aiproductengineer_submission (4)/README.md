# AIVOA – AI-Powered Customer Complaint Management System

A polished full-stack implementation for the AIVOA Round 1 AI Product Engineer (Interns) assignment.

## Stack
- Frontend: React + Redux Toolkit + Vite
- Backend: FastAPI + SQLAlchemy
- AI workflow: LangGraph
- LLM: Google Gemini 2.0 Flash (configurable model name)
- Database: MySQL or PostgreSQL via `DATABASE_URL`
- Optional demo fallback: deterministic mock AI mode so the UI can be demonstrated without an API key

## What is implemented
1. End-to-end complaint logging workflow.
2. Document/text ingestion from the right-side AI assistant (TXT/EML directly, PDF through the FastAPI parser).
3. AI extraction into complaint fields.
4. AI-powered risk assessment (severity, priority, rationale, actions).
5. Completeness checker.
6. Duplicate complaint similarity check.
7. Root-cause and CAPA suggestions.
8. Complaint persistence through FastAPI + SQLAlchemy.
9. Redux state management for form, assistant, loading/error states.
10. Responsive UI closely inspired by the supplied reference screenshot, while not copying it pixel-for-pixel.

## Quick start

### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
uvicorn app.main:app --reload --port 8000
```

Use a MySQL/PostgreSQL connection string in `.env`, for example:
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/aivoa_complaints
# DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/aivoa_complaints
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.0-flash
```

For a no-key demo:
```env
AI_PROVIDER=mock
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

### 3. API documentation
With the backend running, open `http://localhost:8000/docs`.

## Important assignment note
The supplied brief says applicants should understand the AI-generated code and adapt it to the demonstrated workflow. This repository is intentionally structured into small services and UI components so every major part can be explained during the interview.

## Demo credentials
No login is required for this assignment demo.

## Suggested demo flow
See `docs/DEMO_SCRIPT.md` for a 5–10 minute walkthrough covering the complete end-to-end workflow and the AI features.
