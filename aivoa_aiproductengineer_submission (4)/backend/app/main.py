from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routers.complaints import router as complaints_router
from .routers.ai import router as ai_router

app = FastAPI(
    title="AIVOA Complaint Management API",
    version="1.0.0",
    description="AI-assisted customer complaint intake and assessment for pharmaceutical manufacturing.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup() -> None:
    init_db()

@app.get("/health")
def health():
    return {"status": "ok", "service": "aivoa-complaint-api"}

app.include_router(complaints_router, prefix="/api/complaints", tags=["complaints"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai"])
