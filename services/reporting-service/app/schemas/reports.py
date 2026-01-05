from decimal import Decimal
from pydantic import BaseModel

class MonthlySummary(BaseModel):
    user_id: int
    year: int
    month: int
    total: Decimal

class CategoryTotal(BaseModel):
    category: str
    total: Decimal

class RangeTotal(BaseModel):
    user_id: int
    total: Decimal
