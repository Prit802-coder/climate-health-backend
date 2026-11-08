from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class CitizenReport(Base):
    __tablename__ = "citizen_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String(100), nullable=False)
    ward = Column(String(100), nullable=False)
    symptom = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)  # Mild, Moderate, Severe
    desc = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
