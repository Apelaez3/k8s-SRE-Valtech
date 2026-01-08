from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.deps import get_current_user
from app.schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.services.expense_service import ExpenseService
from app.db.session import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(prefix="/expenses", tags=["expenses"],dependencies=[Depends(get_current_user)])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_expense_service(db: Session = Depends(get_db)) -> ExpenseService:
    return ExpenseService(db=db)


def _uid_from_claims(claims: dict) -> int:
    """
    Normaliza el uid que viene del JWT.
    """
    try:
        return int(claims["uid"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token (missing uid)")


def _ensure_owner(expense, uid: int) -> None:
    """
    Bloquea acceso si el gasto no pertenece al usuario autenticado.
    """
    if expense.user_id != uid:
        raise HTTPException(status_code=403, detail="Forbidden")

@router.post("/", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(
    payload: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
    claims: dict = Depends(get_current_user),
):
    uid = int(claims["uid"])
    return service.create_expense(
        user_id=uid,  # ✅ del JWT
        amount=payload.amount,
        category=payload.category,
        description=payload.description,
        expense_date=payload.date,
    )


@router.get("/{expense_id}", response_model=ExpenseRead)
def get_expense(
    expense_id: int,
    service: ExpenseService = Depends(get_expense_service),
    claims: dict = Depends(get_current_user),
):
    uid = _uid_from_claims(claims)

    expense = service.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    _ensure_owner(expense, uid)
    return expense


@router.get("/", response_model=list[ExpenseRead])
def list_expenses(
    category: Optional[str] = Query(default=None),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: ExpenseService = Depends(get_expense_service),
    claims: dict = Depends(get_current_user),
):
    uid = _uid_from_claims(claims)

    # ✅ Ignora user_id del cliente: siempre el del token
    return service.list_expenses(
        user_id=uid,
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
    claims: dict = Depends(get_current_user),
):
    uid = _uid_from_claims(claims)

    expense = service.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    _ensure_owner(expense, uid)

    return service.update_expense(
        expense,
        amount=payload.amount,
        category=payload.category,
        description=payload.description,
        expense_date=payload.date,
    )


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    service: ExpenseService = Depends(get_expense_service),
    claims: dict = Depends(get_current_user),
):
    uid = _uid_from_claims(claims)

    expense = service.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    _ensure_owner(expense, uid)

    service.delete_expense(expense)
    return None
