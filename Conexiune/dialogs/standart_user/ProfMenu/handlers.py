from aiogram.types import Message
from aiogram_dialog import DialogManager
import re

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from Conexiune.db.tables.tables import ProfAdjust
from Conexiune.dialogs.standart_user.ProfMenu.states import ProfMenuSG


async def name_handler(m: Message, MessageInput, manager: DialogManager):
    if re.match(r'^[А-Яа-я]{4,50}$', m.text):
        maker: async_sessionmaker[AsyncSession] = manager.middleware_data['session_maker']
        async with maker() as session:
            async with session.begin():
                user_id = manager.dialog_data['us_pg_id']
                await session.merge(ProfAdjust(user_id=user_id, name=m.text))
    # if p.name:
        # INSERT
    # else:
        # UPDATE


        await manager.switch_to(ProfMenuSG.main)
    else:
        await m.reply('Имя не подходит. Используй только русские буквы')