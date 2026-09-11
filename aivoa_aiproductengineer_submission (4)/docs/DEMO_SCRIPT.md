# AIVOA 5–10 Minute Demo Script

## 0:00–1:00 – Product overview
"This is an AI-powered customer complaint management system designed for pharmaceutical manufacturing. The goal is to reduce manual complaint intake while keeping the QA team in control of traceability, triage, and next actions."

## 1:00–2:00 – UI and architecture
Show the left complaint form and right AI intake assistant. Explain: React handles the UI, Redux keeps complaint state predictable, FastAPI exposes the API, SQLAlchemy persists complaints, and LangGraph orchestrates the AI pipeline.

## 2:00–4:00 – AI intake
Paste `sample_data/sample_complaint.txt` into the assistant and click **Analyze Complaint**. Explain that the AI extracts the customer, product, strength, batch, dates, complaint narrative, patient impact, initial assessment, and priority. The extracted data is immediately hydrated into the editable form.

## 4:00–5:30 – Risk and completeness
Point out the risk score, rationale, and completeness percentage. Explain that the first-pass score is an assistive triage signal, not a regulatory or QA disposition.

## 5:30–7:00 – Bonus AI features
Click **Refresh Full AI Assessment** and show CAPA/root-cause recommendations. Explain that the same complaint object can be passed to separate AI skills without making the UI tightly coupled to model code.

## 7:00–8:00 – Persistence
Click **Save Complaint**. Explain that FastAPI validates the payload and SQLAlchemy stores it in MySQL/PostgreSQL (or SQLite for the zero-setup demo).

## 8:00–9:00 – Explain LangGraph
Walk through `backend/app/services/ai.py`: extract -> risk -> completeness -> END. Mention that Gemini is the production provider and mock mode exists purely to allow deterministic local demonstration without exposing credentials.

## 9:00–10:00 – Engineering notes
Show API docs at `/docs`, then README. Explain that files are deliberately small, the API is RESTful, the UI is responsive, and the implementation is easy to extend with authentication, audit logging, OCR, and regulatory workflows.
