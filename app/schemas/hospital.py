from typing import Optional, List
from pydantic import BaseModel

class HospitalFacilityOut(BaseModel):
    id: str
    name: str
    bedsOccupied: int
    bedsTotal: int
    congestion: str
    alertLevel: str

class HospitalBurdenStatOut(BaseModel):
    date: str
    admissions: int
    expected: int
    temp: float
    pm25: float
