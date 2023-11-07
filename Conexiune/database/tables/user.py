from typing import Optional

from sqlalchemy import BigInteger, String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Conexiune.database.tables.base import Base
from enums import Role


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String)
    first_name: Mapped[Optional[str]] = mapped_column(String)
    role: Mapped[Optional] = mapped_column(Enum(Role))
    prof_adj = relationship(
        'ProfAdjust',
        foreign_keys='ProfAdjust.user_fk',
        lazy='noload',
        back_populates='user_1',
        uselist=False)
    feed_setts = relationship(
        'FeedSettings',
        foreign_keys='FeedSettings.user_fk',
        lazy='noload',
        back_populates='user_2',
        uselist=False)
