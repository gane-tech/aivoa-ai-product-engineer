from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ComplaintBase(BaseModel):
    complaint_source: str = Field(default="Customer Email")
    customer_name: str = ""
    product_name: str = ""
    product_strength: str = ""
    batch_number: str = ""
    manufacturing_date: str = ""
    expiry_date: str = ""
    complaint_details: str = ""
    patient_or_consumer: str = ""
    initial_assessment: str = ""
    priority: str = "Medium"
    status: str = "Pending Triage"

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintOut(ComplaintBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class AIExtraction(BaseModel):
    complaint_source: str = "Customer Email"
    customer_name: str = ""
    product_name: str = ""
    product_strength: str = ""
    batch_number: str = ""
    manufacturing_date: str = ""
    expiry_date: str = ""
    complaint_details: str = ""
    patient_or_consumer: str = ""
    initial_assessment: str = ""
    priority: str = "Medium"

class RiskAssessment(BaseModel):
    risk_level: str
    priority: str
    score: int
    rationale: str
    recommended_actions: list[str]

class CompletenessResult(BaseModel):
    complete: bool
    score: int
    missing_fields: list[str]
    notes: list[str]

class SimilarityResult(BaseModel):
    duplicate: bool
    confidence: int
    matched_complaint_id: Optional[int] = None
    explanation: str

class RootCauseResult(BaseModel):
    likely_causes: list[str]
    capa_recommendations: list[str]
    investigation_questions: list[str]
