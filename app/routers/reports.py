from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.report import CitizenReport
from app.schemas.report import CitizenReportCreate, CitizenReportOut, CitizenReportAnalytics

router = APIRouter(tags=["Citizen Health Reports"])

INITIAL_REPORTS = [
    {"name": "A. K.", "ward": "Ward C", "symptom": "severe_coughing", "severity": "Severe", "desc": "Dense industrial smoke causing asthma exacerbation in children."},
    {"name": "M. R.", "ward": "Ward A", "symptom": "heat_rash", "severity": "Moderate", "desc": "Intense heat indexes causing body rashes and dehydration during afternoon delivery shifts."},
    {"name": "S. T.", "ward": "Ward E", "symptom": "itchy_eyes", "severity": "Mild", "desc": "High pollen allergen spikes causing nasal and ocular irritation."},
    {"name": "D. P.", "ward": "Ward C", "symptom": "breathing_difficulty", "severity": "Severe", "desc": "Heavy particulate smell in the air making breathing shallow."}
]

def seed_reports_if_empty(db: Session):
    count = db.query(CitizenReport).count()
    if count == 0:
        for r in INITIAL_REPORTS:
            db_rep = CitizenReport(
                name=r["name"],
                ward=r["ward"],
                symptom=r["symptom"],
                severity=r["severity"],
                desc=r["desc"]
            )
            db.add(db_rep)
        db.commit()

def _calc_time_ago(created_at: datetime) -> str:
    if not created_at:
        return "Just now"
    # Make timezone aware if needed
    now = datetime.now(timezone.utc)
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    diff = (now - created_at).total_seconds()
    if diff < 60:
        return "Just now"
    elif diff < 3600:
        mins = int(diff // 60)
        return f"{mins} mins ago"
    elif diff < 86400:
        hrs = int(diff // 3600)
        return f"{hrs} hours ago"
    else:
        days = int(diff // 86400)
        return f"{days} days ago"

@router.get("/citizen-reports", response_model=List[CitizenReportOut])
def get_citizen_reports(db: Session = Depends(get_db)):
    seed_reports_if_empty(db)
    reports = db.query(CitizenReport).order_by(CitizenReport.id.desc()).all()
    return [
        CitizenReportOut(
            id=r.id,
            name=r.name,
            ward=r.ward,
            symptom=r.symptom,
            severity=r.severity,
            desc=r.desc,
            time=_calc_time_ago(r.created_at),
            created_at=r.created_at
        ) for r in reports
    ]

@router.post("/citizen-reports", status_code=status.HTTP_201_CREATED)
def submit_citizen_report(report_in: CitizenReportCreate, db: Session = Depends(get_db)):
    db_report = CitizenReport(
        name=report_in.name.strip() or "Anonymous",
        ward=report_in.ward,
        symptom=report_in.symptom,
        severity=report_in.severity,
        desc=report_in.desc.strip()
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return {
        "success": True,
        "report": {
            "id": db_report.id,
            "name": db_report.name,
            "ward": db_report.ward,
            "symptom": db_report.symptom,
            "severity": db_report.severity,
            "desc": db_report.desc,
            "time": "Just now"
        }
    }

@router.get("/citizen-reports/stats", response_model=CitizenReportAnalytics)
def get_report_statistics(db: Session = Depends(get_db)):
    seed_reports_if_empty(db)
    reports = db.query(CitizenReport).all()
    total = len(reports)
    severe = sum(1 for r in reports if r.severity.lower() == "severe")
    respiratory = sum(1 for r in reports if r.symptom in ["breathing_difficulty", "severe_coughing"])
    thermal = sum(1 for r in reports if r.symptom in ["heat_rash", "heat_stroke"])
    allergic = sum(1 for r in reports if r.symptom in ["itchy_eyes", "allergic_rhinitis"])

    return CitizenReportAnalytics(
        total_reports=total,
        severe_count=severe,
        respiratory_count=respiratory,
        thermal_count=thermal,
        allergic_count=allergic
    )
