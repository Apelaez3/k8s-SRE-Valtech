from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

class ExpenseCreate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    date: date

class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = Field(default=None, gt=0)
    category: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    date: Optional[date] = None

class ExpenseRead(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    category: str
    description: Optional[str]
    date: date

    class Config:
        from_attributes = True

