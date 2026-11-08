from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class WeatherCache(Base):
    __tablename__ = "weather_cache"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), unique=True, index=True, nullable=False)
    weather_json = Column(Text, nullable=False)
    aqi_json = Column(Text, nullable=False)
    health_index = Column(Integer, nullable=False)
    cached_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
