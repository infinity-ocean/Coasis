from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from middlewares.user_redis import role_redis, handle_non_redis


class db_middleware(BaseMiddleware):
    """This middleware throw a Database class to handler"""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        maker: async_sessionmaker[AsyncSession] = data['maker']
        async with maker() as session:
            redis = data['redis']
            role = await role_redis(event.from_user.id, redis)
            if role:
                data['role'] = role
            else:
                role = await handle_non_redis(session, event, redis, data)
                data['role'] = role

            data['session'] = session

            return await handler(event, data)
