from datetime import date as dt_date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    category: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # ✅ tipo correcto (dt_date) + columna SQLAlchemy Date
    date: Mapped[dt_date] = mapped_column(Date, nullable=False)