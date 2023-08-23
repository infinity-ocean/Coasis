from typing import Optional

from sqlalchemy import Integer, ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from Conexiune.database.tables.base import Base


class ProfAdjust(Base):
    __tablename__ = 'profiles_adjust'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)

    photo: Mapped[Optional[str]] = mapped_column(String)
    name: Mapped[Optional[str]] = mapped_column(String(50))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    sex: Mapped[Optional[str]] = mapped_column(String(1))
    # goal: Mapped[Optional[str]] = mapped_column(JSONB)
    location: Mapped[Optional[str]] = mapped_column(String(40))
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    descr: Mapped[Optional[str]] = mapped_column(String(824))
