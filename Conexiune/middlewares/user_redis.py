from enum import Enum
from typing import Dict, Any

from aiogram.types import Message, CallbackQuery
from redis.asyncio.client import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Conexiune.database.tables.feed_settings import FeedSettings
from Conexiune.database.tables.prof_adjust import ProfAdjust
from Conexiune.database.tables.user import User
from enums import Role


async def registrate_u(session: AsyncSession, event, back):
    u_reg = User(
        tg_id=event.id, username=event.username,
        first_name=event.first_name, role=1)  # ?
    u_reg.prof_adj = ProfAdjust()
    u_reg.feed_setts = FeedSettings()
    await session.merge(u_reg)
    slct_u_fresh = select(User).where(User.tg_id == event.id).options(selectinload(User.prof_adj))
    _u_fresh = await session.scalars(slct_u_fresh)
    u_fresh = _u_fresh.one_or_none()
    back['u_id'] = u_fresh.id
    return u_fresh


async def role_redis(tg_id: int,
                     redis: Redis) -> bool:
    role = await redis.get(name='user_role:' + str(tg_id))
    return role if role else False


async def handle_non_redis(session: AsyncSession,
                           event: Message | CallbackQuery,
                           redis: Redis,
                           data: Dict[str, Any]) -> Role:
    async with session.begin():
        u_pg = (await session.execute(select(User).where(User.tg_id == event.from_user.id))).one_or_none()
        if u_pg:
            await redis.set(name='user_role:' + str(event.from_user.id), value=u_pg.role)
            # IS IT ACCEPTS ENUM or CONVERT TO INT?
            return u_pg.role
        else:
            await registrate_u(session, event, data)
            return Role(1)
