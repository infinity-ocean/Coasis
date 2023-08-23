from typing import Optional

from sqlalchemy import BigInteger, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Conexiune.database.tables.base import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String)
    first_name: Mapped[Optional[str]] = mapped_column(String)

    prof_adj: Mapped['ProfAdjust'] = relationship(uselist=False, backref='user')


# class ProfAdjust(Base):
#     __tablename__ = 'profiles_adjust'
#     __table_args__ = {'extend_existing': True}
#
#     id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
#
#     photo: Mapped[Optional[str]] = mapped_column(String)
#     name: Mapped[Optional[str]] = mapped_column(String(50))
#     age: Mapped[Optional[int]] = mapped_column(Integer)
#     sex: Mapped[Optional[str]] = mapped_column(String(1))
#     # goal: Mapped[Optional[str]] = mapped_column(JSONB)
#     location: Mapped[Optional[str]] = mapped_column(String(40))
#     latitude: Mapped[Optional[float]] = mapped_column(Float)
#     longitude: Mapped[Optional[float]] = mapped_column(Float)
#     descr: Mapped[Optional[str]] = mapped_column(String(824))

# class FeedSettings(Base):
#     __tablename__ = 'feed_settings'
#     id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
#
#     # sex = mapped_column(enum.Enum)
