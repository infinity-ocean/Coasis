from enum import Enum
from typing import Dict, Any

from aiogram.types import Message, CallbackQuery
from redis.asyncio.client import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.tables.user import User
from database.tables.prof_adjust import ProfAdjust
from database.tables.feed_settings import FeedSettings
from enums import Role


async def registrate_u(session: AsyncSession, event: Message | CallbackQuery, data: Dict[str, Any]):
    u_reg = User(  # default attributes for registration
        tg_id=event.from_user.id, 
        username=event.from_user.username,
        first_name=event.from_user.first_name,
        role=Role(1)) 
    u_reg.prof_adj = ProfAdjust()
    u_reg.feed_setts = FeedSettings()
    await session.merge(u_reg)
    # select for user's ID
    slct_u_fresh = select(User).where(User.tg_id == event.from_user.id).options(selectinload(User.prof_adj))
    _u_fresh = await session.scalars(slct_u_fresh)
    u_fresh = _u_fresh.one()  
    data['u_id'] = u_fresh.id


async def handle_zero_role(session: AsyncSession,
                           event: Message | CallbackQuery,
                           data: Dict[str, Any]) -> int:
    async with session.begin():
        u_pg = (await session.scalars(select(User).where(User.tg_id == event.from_user.id))).one_or_none()
        if u_pg:  # роли нету в оперативке, но есть в пг
            return u_pg.role.value
        else:  # user doesn't exist
            await registrate_u(session, event, data)
            return Role(1).value
