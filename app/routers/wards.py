from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.ward import WardTelemetry
from app.schemas.ward import WardOut

router = APIRouter(tags=["Ward Telemetry"])

DEFAULT_WARDS = [
    {"ward_id": "ward-a", "name": "Downtown District (Ward A)", "risk": "high", "score": 82, "temp": 34.0, "pm25": 145.0, "pop": "42,000", "seniors": "18%", "hospitals": 3, "alert": "Heat Wave & Ozone Warning"},
    {"ward_id": "ward-b", "name": "Westside Residential (Ward B)", "risk": "medium", "score": 55, "temp": 31.0, "pm25": 85.0, "pop": "68,000", "seniors": "12%", "hospitals": 1, "alert": "Moderate Allergy Spikes"},
    {"ward_id": "ward-c", "name": "Industrial Hub (Ward C)", "risk": "high", "score": 89, "temp": 35.0, "pm25": 198.0, "pop": "29,000", "seniors": "7%", "hospitals": 2, "alert": "Critical Air Quality (PM2.5)"},
    {"ward_id": "ward-d", "name": "Southlake Greenbelt (Ward D)", "risk": "low", "score": 28, "temp": 28.0, "pm25": 32.0, "pop": "35,000", "seniors": "14%", "hospitals": 1, "alert": "No active warnings"},
    {"ward_id": "ward-e", "name": "North Heights (Ward E)", "risk": "medium", "score": 48, "temp": 30.0, "pm25": 72.0, "pop": "54,000", "seniors": "22%", "hospitals": 2, "alert": "Elevated Pollen Spores"},
    {"ward_id": "ward-f", "name": "Eastside Meadows (Ward F)", "risk": "low", "score": 22, "temp": 27.0, "pm25": 25.0, "pop": "31,000", "seniors": "10%", "hospitals": 0, "alert": "No active warnings"}
]

def seed_wards_if_empty(db: Session):
    count = db.query(WardTelemetry).count()
    if count == 0:
        for w in DEFAULT_WARDS:
            db_w = WardTelemetry(
                ward_id=w["ward_id"],
                name=w["name"],
                risk=w["risk"],
                score=w["score"],
                temp=w["temp"],
                pm25=w["pm25"],
                pop=w["pop"],
                seniors=w["seniors"],
                hospitals=w["hospitals"],
                alert=w["alert"]
            )
            db.add(db_w)
        db.commit()

@router.get("/ward-telemetry", response_model=List[WardOut])
def get_wards(db: Session = Depends(get_db)):
    print("[WARD] Request started")

    print("[WARD] Starting seed check")
    seed_wards_if_empty(db)
    print("[WARD] Seed check completed")

    print("[WARD] Starting database query")
    wards = db.query(WardTelemetry).all()
    print(f"[WARD] Query completed. Records: {len(wards)}")

    return [
        WardOut(
            id=w.ward_id,
            name=w.name,
            risk=w.risk,
            score=w.score,
            temp=w.temp,
            pm25=w.pm25,
            pop=w.pop,
            seniors=w.seniors,
            hospitals=w.hospitals,
            alert=w.alert
        ) for w in wards
    ]

@router.get("/ward-telemetry/{ward_id}", response_model=WardOut)
def get_ward_by_id(ward_id: str, db: Session = Depends(get_db)):
    seed_wards_if_empty(db)
    w = db.query(WardTelemetry).filter(WardTelemetry.ward_id == ward_id).first()
    if not w:
        raise HTTPException(status_code=404, detail="Ward not found.")
    return WardOut(
        id=w.ward_id,
        name=w.name,
        risk=w.risk,
        score=w.score,
        temp=w.temp,
        pm25=w.pm25,
        pop=w.pop,
        seniors=w.seniors,
        hospitals=w.hospitals,
        alert=w.alert
    )
