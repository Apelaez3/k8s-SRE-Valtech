from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_expense_service(db: Session = Depends(get_db)) -> ExpenseService:
    return ExpenseService(db=db)


@router.post("/", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(payload: ExpenseCreate, service: ExpenseService = Depends(get_expense_service)):
    return service.create_expense(
        user_id=payload.user_id,
        amount=payload.amount,
        category=payload.category,
        description=payload.description,
        expense_date=payload.date,
    )


@router.get("/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_id: int, service: ExpenseService = Depends(get_expense_service)):
    expense = service.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.get("/", response_model=list[ExpenseRead])
def list_expenses(
    user_id: Optional[int] = Query(default=None),
    category: Optional[str] = Query(default=None),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.list_expenses(
        user_id=user_id,
        category=category,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )


@router.patch("/{expense_id}", response_model=ExpenseRead)
def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    service: ExpenseService = Depends(get_expense_service),
):
    expense = service.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return service.update_expense(
        expense,
        amount=payload.amount,
        category=payload.category,
        description=payload.description,
        expense_date=payload.date,
    )


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, service: ExpenseService = Depends(get_expense_service)):
    expense = service.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    service.delete_expense(expense)
    return None