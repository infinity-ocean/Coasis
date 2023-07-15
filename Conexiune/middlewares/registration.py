from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from Conexiune.db.tables.tables import User

class RegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            Update: Message | CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        maker: async_sessionmaker[AsyncSession] = data["session_maker"]
        # В переменую result записывается User.
        async with maker() as session:
            async with session.begin():
                stmt = select(User).where(User.tg_id == Update.from_user.id)
                result = await session.scalars(stmt)
                if result.one_or_none() == None:

                    session.add(User(
                        tg_id=Update.from_user.id,
                        username=Update.from_user.username,
                        first_name=Update.from_user.first_name
                    ))
                    await Update.answer('regmdw: Пользователь был записан в БД')
                else:
                    pass
        return await handler(Update, data)
