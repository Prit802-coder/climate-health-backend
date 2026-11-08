from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class CitizenReportCreate(BaseModel):
    name: str = "Anonymous"
    ward: str
    symptom: str
    severity: str
    desc: str

class CitizenReportOut(BaseModel):
    id: int
    name: str
    ward: str
    symptom: str
    severity: str
    desc: str
    time: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CitizenReportAnalytics(BaseModel):
    total_reports: int
    severe_count: int
    respiratory_count: int
    thermal_count: int
    allergic_count: int
