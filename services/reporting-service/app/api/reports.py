from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.reporting_service import ReportingService
from app.schemas.reports import MonthlySummary, CategoryTotal, RangeTotal

# ❌ SIN prefix="/reports"
router = APIRouter(tags=["reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_service(db: Session = Depends(get_db)):
    return ReportingService(db)

@router.get("/monthly", response_model=MonthlySummary)
def monthly_summary(user_id: int, year: int, month: int, svc=Depends(get_service)):
    total = svc.monthly_summary(user_id, year, month)
    return {"user_id": user_id, "year": year, "month": month, "total": total}

@router.get("/by-category", response_model=list[CategoryTotal])
def by_category(user_id: int, svc=Depends(get_service)):
    rows = svc.by_category(user_id)
    return [{"category": c, "total": t} for c, t in rows]

@router.get("/range", response_model=RangeTotal)
def range_total(user_id: int, start: date, end: date, svc=Depends(get_service)):
    total = svc.total_between(user_id, start, end)
    return {"user_id": user_id, "total": total}

