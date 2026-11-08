from typing import Optional, Dict, List, Any
from pydantic import BaseModel

class PollutantSubIndices(BaseModel):
    pm2_5: Optional[int] = 0
    pm10: Optional[int] = 0
    o3: Optional[int] = 0
    no2: Optional[int] = 0
    so2: Optional[int] = 0
    co: Optional[int] = 0

class WeatherResponse(BaseModel):
    city: str
    country: Optional[str] = ""
    temperature: float
    feels_like: float
    humidity: int
    condition: str
    description: str
    wind_speed: float
    uv: float = 4.0
    aqi: int
    aqi_label: str
    allergen: str = "Medium"
    components: Dict[str, float] = {}
    sub_indices: Optional[PollutantSubIndices] = None

class ForecastItem(BaseModel):
    day: str
    date: str
    index: int
    temp: float
    aqi: int
    uv: float
    allergen: str
    condition: str
    desc: str

class HourlyRiskSlot(BaseModel):
    time: str
    label: str
    temp: float
    aqi: int
    uv: float
    wind: float
    status: str
    color: str
    desc: str
