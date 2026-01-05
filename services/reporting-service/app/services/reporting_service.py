from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models.expense import Expense

class ReportingService:
    def __init__(self, db: Session):
        self.db = db

    def monthly_summary(self, user_id: int, year: int, month: int):
        return (
            self.db.query(func.sum(Expense.amount).label("total"))
            .filter(
                Expense.user_id == user_id,
                func.strftime("%Y", Expense.date) == str(year),
                func.strftime("%m", Expense.date) == f"{month:02d}",
            )
            .scalar()
            or 0
        )

    def by_category(self, user_id: int):
        return (
            self.db.query(
                Expense.category,
                func.sum(Expense.amount).label("total"),
            )
            .filter(Expense.user_id == user_id)
            .group_by(Expense.category)
            .all()
        )

    def total_between(self, user_id: int, start: date, end: date):
        return (
            self.db.query(func.sum(Expense.amount))
            .filter(
                Expense.user_id == user_id,
                Expense.date.between(start, end),
            )
            .scalar()
            or 0
        )
