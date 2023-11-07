from redis.asyncio.client import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.user import User


async def user_redis(tg_id: int, session: AsyncSession, redis: Redis) -> bool:
    u_red = await redis.get(name='user_exists:' + str(tg_id))
    if u_red:
        return True
    else:
        async with session.begin():
            u_pg = (await session.execute(select(User).where(User.tg_id == tg_id))).one_or_none()
            if u_pg:
                await redis.set(name='user_exists:' + str(tg_id), value=1)
                return True
            else:
                return False
