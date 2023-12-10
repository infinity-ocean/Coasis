from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from middlewares.user_redis import handle_zero_role


class ses_reg_role_mdw(BaseMiddleware):
    """This middleware throw a Database class to handler"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        maker: async_sessionmaker[AsyncSession] = data['maker']
        async with maker() as session:
            # ROLE
            if 'role' in data:
                pass
            else:
                role = await handle_zero_role(session, event, data)
                data['role'] = role
            # SESSION
            data['session'] = session

            return await handler(event, data)
