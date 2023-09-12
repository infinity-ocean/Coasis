from typing import Optional

from sqlalchemy import Integer, ForeignKey, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Conexiune.database.tables.base import Base


class FeedSettings(Base):
    __tablename__ = 'feed_settings'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    user_2 = relationship('User',
                          foreign_keys=user_fk,
                          lazy='noload',
                          back_populates='feed_setts',
                          uselist=False)
    sex: Mapped[Optional[str]] = mapped_column(String(1))
    min_age: Mapped[Optional[int]] = mapped_column(SmallInteger)
    max_age: Mapped[Optional[int]] = mapped_column(SmallInteger)
    location: Mapped[Optional[str]] = mapped_column(String(1))

    # convert to enum, and in other tables
