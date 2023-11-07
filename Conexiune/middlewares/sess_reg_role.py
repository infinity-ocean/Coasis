from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from middlewares.user_redis import user_redis


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
            if await user_redis(event.from_user.id, session, redis):
                pass
            # if redis.user != None -> pass
            # else: role = select(event.id) (return user role or None)
            # if role == def ->
            # if role == prem ->
            # if role == none ->
            # if role == mod ->

            data['session'] = session

            return await handler(event, data)
