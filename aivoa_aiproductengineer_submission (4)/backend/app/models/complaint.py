from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    complaint_source: Mapped[str] = mapped_column(String(120))
    customer_name: Mapped[str] = mapped_column(String(200))
    product_name: Mapped[str] = mapped_column(String(200))
    product_strength: Mapped[str] = mapped_column(String(120), default="")
    batch_number: Mapped[str] = mapped_column(String(120), default="")
    manufacturing_date: Mapped[str] = mapped_column(String(50), default="")
    expiry_date: Mapped[str] = mapped_column(String(50), default="")
    complaint_details: Mapped[str] = mapped_column(Text)
    patient_or_consumer: Mapped[str] = mapped_column(Text, default="")
    initial_assessment: Mapped[str] = mapped_column(Text, default="")
    priority: Mapped[str] = mapped_column(String(30), default="Medium")
    status: Mapped[str] = mapped_column(String(50), default="Pending Triage")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
