from typing import Optional

from sqlalchemy import BigInteger, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Conexiune.database.tables.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String)
    first_name: Mapped[Optional[str]] = mapped_column(String)

    prof_adj: Mapped['ProfAdjust'] = relationship(uselist=False)


class ProfAdjust(Base):
    __tablename__ = 'profiles_adjust'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    photo: Mapped[Optional[str]] = mapped_column(String)
    name: Mapped[Optional[str]] = mapped_column(String(50))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    sex: Mapped[Optional[str]] = mapped_column(String(1))
    # goal: Mapped[Optional[str]] = mapped_column(JSONB)  # turn to simple json if errors occurs
    # latitude: Mapped[Optional[float]] = mapped_column(Float)
    # longitude: Mapped[Optional[float]] = mapped_column(Float)
    descr: Mapped[Optional[str]] = mapped_column(String(824))
