from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.hospital import HospitalFacility, HospitalBurdenStat
from app.schemas.hospital import HospitalFacilityOut, HospitalBurdenStatOut

router = APIRouter(tags=["Hospital Burden Dashboard"])

DEFAULT_FACILITIES = [
    {"facility_id": "city-general", "name": "Metropolitan General Hospital", "beds_occupied": 142, "beds_total": 180, "congestion": "High", "alert_level": "yellow"},
    {"facility_id": "westside-clinic", "name": "Westside Pulmonary Center", "beds_occupied": 45, "beds_total": 85, "congestion": "Moderate", "alert_level": "green"},
    {"facility_id": "pediatric-emergency", "name": "Saint Jude Pediatric Emergency", "beds_occupied": 72, "beds_total": 80, "congestion": "Critical", "alert_level": "red"}
]

DEFAULT_BURDEN_STATS = {
    "city-general": [
        {"day": "Mon", "admissions": 18, "expected": 15, "temp": 24.0, "pm25": 48.0},
        {"day": "Tue", "admissions": 22, "expected": 17, "temp": 26.0, "pm25": 58.0},
        {"day": "Wed", "admissions": 31, "expected": 26, "temp": 31.0, "pm25": 82.0},
        {"day": "Thu", "admissions": 42, "expected": 38, "temp": 34.0, "pm25": 110.0},
        {"day": "Fri", "admissions": 58, "expected": 48, "temp": 36.0, "pm25": 135.0},
        {"day": "Sat", "admissions": 39, "expected": 32, "temp": 27.0, "pm25": 88.0},
        {"day": "Sun", "admissions": 24, "expected": 20, "temp": 22.0, "pm25": 42.0}
    ],
    "westside-clinic": [
        {"day": "Mon", "admissions": 8, "expected": 7, "temp": 24.0, "pm25": 48.0},
        {"day": "Tue", "admissions": 11, "expected": 9, "temp": 26.0, "pm25": 58.0},
        {"day": "Wed", "admissions": 16, "expected": 14, "temp": 31.0, "pm25": 82.0},
        {"day": "Thu", "admissions": 24, "expected": 20, "temp": 34.0, "pm25": 110.0},
        {"day": "Fri", "admissions": 32, "expected": 25, "temp": 36.0, "pm25": 135.0},
        {"day": "Sat", "admissions": 19, "expected": 17, "temp": 27.0, "pm25": 88.0},
        {"day": "Sun", "admissions": 10, "expected": 9, "temp": 22.0, "pm25": 42.0}
    ],
    "pediatric-emergency": [
        {"day": "Mon", "admissions": 14, "expected": 12, "temp": 24.0, "pm25": 48.0},
        {"day": "Tue", "admissions": 18, "expected": 15, "temp": 26.0, "pm25": 58.0},
        {"day": "Wed", "admissions": 28, "expected": 22, "temp": 31.0, "pm25": 82.0},
        {"day": "Thu", "admissions": 36, "expected": 30, "temp": 34.0, "pm25": 110.0},
        {"day": "Fri", "admissions": 49, "expected": 40, "temp": 36.0, "pm25": 135.0},
        {"day": "Sat", "admissions": 30, "expected": 26, "temp": 27.0, "pm25": 88.0},
        {"day": "Sun", "admissions": 18, "expected": 15, "temp": 22.0, "pm25": 42.0}
    ]
}

def seed_hospital_if_empty(db: Session):
    if db.query(HospitalFacility).count() == 0:
        for f in DEFAULT_FACILITIES:
            db_f = HospitalFacility(
                facility_id=f["facility_id"],
                name=f["name"],
                beds_occupied=f["beds_occupied"],
                beds_total=f["beds_total"],
                congestion=f["congestion"],
                alert_level=f["alert_level"]
            )
            db.add(db_f)
        db.commit()

    if db.query(HospitalBurdenStat).count() == 0:
        for fac_id, stats in DEFAULT_BURDEN_STATS.items():
            for s in stats:
                db_s = HospitalBurdenStat(
                    facility_id=fac_id,
                    day_name=s["day"],
                    admissions=s["admissions"],
                    expected=s["expected"],
                    temp=s["temp"],
                    pm25=s["pm25"]
                )
                db.add(db_s)
        db.commit()

@router.get("/hospital/facilities", response_model=List[HospitalFacilityOut])
def get_facilities(db: Session = Depends(get_db)):
    seed_hospital_if_empty(db)
    facilities = db.query(HospitalFacility).all()
    return [
        HospitalFacilityOut(
            id=f.facility_id,
            name=f.name,
            bedsOccupied=f.beds_occupied,
            bedsTotal=f.beds_total,
            congestion=f.congestion,
            alertLevel=f.alert_level
        ) for f in facilities
    ]

@router.get("/hospital-burden", response_model=List[HospitalBurdenStatOut])
def get_burden_stats(
    facilityId: str = Query("city-general", description="Facility identifier"),
    db: Session = Depends(get_db)
):
    seed_hospital_if_empty(db)
    stats = db.query(HospitalBurdenStat).filter(HospitalBurdenStat.facility_id == facilityId).all()
    if not stats:
        # Fallback to city-general
        stats = db.query(HospitalBurdenStat).filter(HospitalBurdenStat.facility_id == "city-general").all()

    return [
        HospitalBurdenStatOut(
            date=s.day_name,
            admissions=s.admissions,
            expected=s.expected,
            temp=s.temp,
            pm25=s.pm25
        ) for s in stats
    ]
