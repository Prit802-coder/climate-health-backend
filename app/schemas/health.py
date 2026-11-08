from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class HealthProfileInput(BaseModel):
    age: int = 30
    occupation: str = "indoor"
    conditions: Optional[Dict[str, bool]] = None

class EnvironmentInput(BaseModel):
    aqi: Optional[float] = 68.0
    temp: Optional[float] = 24.0
    uv: Optional[float] = 4.0
    humidity: Optional[float] = 60.0
    pollen: Optional[float] = 25.0

class RiskAssessmentRequest(BaseModel):
    profile: HealthProfileInput
    environment: Optional[EnvironmentInput] = None

class RiskAssessmentResponse(BaseModel):
    score: int
    level: str  # Low, Moderate, Extreme
    color: str
    ring: str
    modifiers: List[str]
    source: str = "FastAPI Climate-Health Predictive Engine"

class HealthIndexCalcRequest(BaseModel):
    aqi: float
    temp: float
    uv: float
    pollen: float

class HealthIndexResponse(BaseModel):
    climate_health_index: int
    risk_level: str
    recommendation: str
    category: Optional[str] = None
    breakdown: Optional[Dict[str, float]] = None
