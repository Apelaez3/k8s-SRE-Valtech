from datetime import date
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.expense import Expense


class ExpenseService:
    def __init__(self, db: Session):
        self.db = db

    def create_expense(
        self,
        user_id: int,
        amount: Decimal,
        category: str,
        description: Optional[str],
        expense_date: date,
    ) -> Expense:
        expense = Expense(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            date=expense_date,
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_expense(self, expense_id: int) -> Optional[Expense]:
        return self.db.query(Expense).filter(Expense.id == expense_id).first()

    def list_expenses(
        self,
        user_id: Optional[int] = None,
        category: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Expense]:
        q = self.db.query(Expense)

        if user_id is not None:
            q = q.filter(Expense.user_id == user_id)
        if category is not None:
            q = q.filter(Expense.category == category)
        if date_from is not None:
            q = q.filter(Expense.date >= date_from)
        if date_to is not None:
            q = q.filter(Expense.date <= date_to)

        return q.order_by(Expense.date.desc(), Expense.id.desc()).offset(offset).limit(limit).all()

    def update_expense(
        self,
        expense: Expense,
        amount: Optional[Decimal] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        expense_date: Optional[date] = None,
    ) -> Expense:
        if amount is not None:
            expense.amount = amount
        if category is not None:
            expense.category = category
        if description is not None:
            expense.description = description
        if expense_date is not None:
            expense.date = expense_date

        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete_expense(self, expense: Expense) -> None:
        self.db.delete(expense)
        self.db.commit()