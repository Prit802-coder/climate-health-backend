from fastapi import APIRouter, Query, HTTPException, Body
from typing import Dict, Any, Optional
from app.services.weather_service import get_city_weather_and_aqi
from app.services.health_engine import (
    calculate_climate_health_index,
    calculate_personalized_risk,
    calculate_safe_time_slots
)
from app.schemas.health import (
    RiskAssessmentRequest,
    RiskAssessmentResponse,
    HealthIndexCalcRequest,
    HealthIndexResponse
)

router = APIRouter(tags=["Climate Health Index & Bio-Risk"])

@router.get("/health-index")
async def get_health_index(city: str = Query("New Delhi", description="City name to evaluate")):
    if not city.strip():
        raise HTTPException(status_code=400, detail="City name is required.")
    try:
        weather_data = await get_city_weather_and_aqi(city.strip())
        hi_result = calculate_climate_health_index(
            aqi=weather_data["aqi"],
            temp=weather_data["temperature"],
            uv=weather_data["uv"],
            pollen=30.0 if weather_data["allergen"] == "High" else 15.0
        )
        return {
            **weather_data,
            "temp": weather_data["temperature"],
            **hi_result
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/health-index/calculate", response_model=HealthIndexResponse)
def calculate_custom_health_index(payload: HealthIndexCalcRequest):
    result = calculate_climate_health_index(
        aqi=payload.aqi,
        temp=payload.temp,
        uv=payload.uv,
        pollen=payload.pollen
    )
    return HealthIndexResponse(
        climate_health_index=result["climate_health_index"],
        risk_level=result["risk_level"],
        recommendation=result["recommendation"],
        category=result["description"],
        breakdown=result["breakdown"]
    )

@router.post("/risk-assessment", response_model=RiskAssessmentResponse)
def calculate_risk_assessment(payload: RiskAssessmentRequest):
    profile_dict = {
        "age": payload.profile.age,
        "occupation": payload.profile.occupation,
        "conditions": payload.profile.conditions or {}
    }
    env_dict = {
        "aqi": payload.environment.aqi if payload.environment else 68.0,
        "temp": payload.environment.temp if payload.environment else 24.0,
        "uv": payload.environment.uv if payload.environment else 4.0,
        "humidity": payload.environment.humidity if payload.environment else 60.0
    }
    result = calculate_personalized_risk(profile_dict, env_dict)
    return RiskAssessmentResponse(**result)

@router.get("/safe-time")
async def get_safe_time_planner(
    city: str = Query("New Delhi"),
    age: int = Query(30),
    occupation: str = Query("indoor"),
    asthma: bool = Query(False),
    cardio: bool = Query(False),
    allergies: bool = Query(False),
    copd: bool = Query(False)
):
    try:
        w_data = await get_city_weather_and_aqi(city.strip())
        profile = {
            "age": age,
            "occupation": occupation,
            "conditions": {
                "asthma": asthma,
                "cardiovascular": cardio,
                "allergies": allergies,
                "copd": copd
            }
        }
        slots = calculate_safe_time_slots(profile, w_data["temperature"], float(w_data["aqi"]))
        return {"city": w_data["city"], "slots": slots}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
