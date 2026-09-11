from fastapi import APIRouter
from ..services.ai import complete, duplicate_check, extract, risk, root_cause, run_pipeline
from ..schemas import AIExtraction, CompletenessResult, RiskAssessment, RootCauseResult
from pydantic import BaseModel
from fastapi import File, UploadFile

router = APIRouter()

class TextRequest(BaseModel):
    text: str

class DataRequest(BaseModel):
    data: dict

@router.post("/extract", response_model=AIExtraction)
def ai_extract(payload: TextRequest):
    return extract(payload.text)

@router.post("/risk", response_model=RiskAssessment)
def ai_risk(payload: DataRequest):
    return risk(payload.data)

@router.post("/completeness", response_model=CompletenessResult)
def ai_completeness(payload: DataRequest):
    return complete(payload.data)

@router.post("/root-cause", response_model=RootCauseResult)
def ai_root_cause(payload: DataRequest):
    return root_cause(payload.data)

@router.post("/pipeline")
def ai_pipeline(payload: TextRequest):
    return run_pipeline(payload.text)


@router.post("/extract-file", response_model=AIExtraction)
async def ai_extract_file(file: UploadFile = File(...)):
    data = await file.read()
    name = (file.filename or "").lower()
    text = ""
    if name.endswith(".pdf"):
        from io import BytesIO
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(data))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
    else:
        text = data.decode("utf-8", errors="ignore")
    return extract(text[:12000])


@router.post("/duplicate")
def ai_duplicate(payload: DataRequest):
    from ..database import SessionLocal
    from ..models.complaint import Complaint
    db = SessionLocal()
    try:
        rows = db.query(Complaint).order_by(Complaint.created_at.desc()).limit(50).all()
        existing = [r.__dict__ for r in rows]
        return duplicate_check(payload.data, existing)
    finally:
        db.close()
