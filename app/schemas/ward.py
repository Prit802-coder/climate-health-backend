from pydantic import BaseModel

class WardOut(BaseModel):
    id: str
    name: str
    risk: str
    score: int
    temp: float
    pm25: float
    pop: str
    seniors: str
    hospitals: int
    alert: str
