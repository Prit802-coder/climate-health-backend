from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class HospitalFacility(Base):
    __tablename__ = "hospital_facilities"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    beds_occupied = Column(Integer, nullable=False, default=0)
    beds_total = Column(Integer, nullable=False, default=100)
    congestion = Column(String(50), default="Moderate")  # High, Moderate, Critical, Low
    alert_level = Column(String(50), default="yellow")   # red, yellow, green

class HospitalBurdenStat(Base):
    __tablename__ = "hospital_burden_stats"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(String(50), index=True, nullable=False)
    day_name = Column(String(20), nullable=False)  # Mon, Tue, Wed, etc.
    admissions = Column(Integer, nullable=False)
    expected = Column(Integer, nullable=False)
    temp = Column(Float, nullable=False)
    pm25 = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
