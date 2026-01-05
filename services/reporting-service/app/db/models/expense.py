from datetime import date as dt_date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    category: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    date: Mapped[dt_date] = mapped_column(Date, index=True)
