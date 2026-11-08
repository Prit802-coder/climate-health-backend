from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class WardTelemetry(Base):
    __tablename__ = "ward_telemetry"

    id = Column(Integer, primary_key=True, index=True)
    ward_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    risk = Column(String(50), nullable=False)  # high, medium, low
    score = Column(Integer, nullable=False)
    temp = Column(Float, nullable=False)
    pm25 = Column(Float, nullable=False)
    pop = Column(String(50), nullable=False)
    seniors = Column(String(50), nullable=False)
    hospitals = Column(Integer, nullable=False, default=1)
    alert = Column(String(255), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
