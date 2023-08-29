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
    # TODO: to deal up with relationships
    prof_adj: Mapped['ProfAdjust'] = relationship(
        uselist=False,
        cascade='save-update',
        lazy='joined',
        back_populates='user')
    feed_setts: Mapped['FeedSettings'] = relationship(
        uselist=False,
        cascade='save-update',
        lazy='joined',
        back_populates='user')
