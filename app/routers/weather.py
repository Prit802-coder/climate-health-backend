from app.services.weather_service import (
    get_city_weather_and_aqi,
    get_city_forecast,
    get_city_hourly_forecast
)
from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any
from app.services.weather_service import get_city_weather_and_aqi, get_city_forecast

router = APIRouter(tags=["Weather & AQI"])

@router.get("/weather")
async def get_weather(city: str = Query("New Delhi", description="City name to fetch telemetry")):
    if not city.strip():
        raise HTTPException(status_code=400, detail="City name is required.")
    try:
        data = await get_city_weather_and_aqi(city.strip())
        # Add alias 'temp' for frontend components expecting data.temp
        data["temp"] = data["temperature"]
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather: {str(e)}")

@router.get("/forecast")
async def get_forecast(city: str = Query("New Delhi", description="City name to fetch 7-day forecast")):
    try:
        forecast_list = await get_city_forecast(city.strip())
        return forecast_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch forecast: {str(e)}")

@router.get("/air-quality")
async def get_air_quality(city: str = Query("New Delhi", description="City name for AQI telemetry")):
    try:
        data = await get_city_weather_and_aqi(city.strip())
        return {
            "city": data["city"],
            "aqi": data["aqi"],
            "aqi_label": data["aqi_label"],
            "components": data["components"],
            "sub_indices": data["sub_indices"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forecast/hourly")
async def get_hourly_forecast(
    city: str = Query("New Delhi", description="City name")
):
    if not city.strip():
        raise HTTPException(
            status_code=400,
            detail="City name is required."
        )

    try:
        return await get_city_hourly_forecast(city.strip())

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch hourly forecast: {str(e)}"
        )
