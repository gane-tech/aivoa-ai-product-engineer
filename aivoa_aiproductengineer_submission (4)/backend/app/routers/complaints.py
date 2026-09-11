from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.complaint import Complaint
from ..schemas import ComplaintCreate, ComplaintOut

router = APIRouter()

@router.post("", response_model=ComplaintOut)
def create_complaint(payload: ComplaintCreate, db: Session = Depends(get_db)):
    item = Complaint(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("", response_model=list[ComplaintOut])
def list_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).order_by(Complaint.created_at.desc()).limit(50).all()

@router.get("/{complaint_id}", response_model=ComplaintOut)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    item = db.get(Complaint, complaint_id)
    if not item:
        raise HTTPException(404, "Complaint not found")
    return item
