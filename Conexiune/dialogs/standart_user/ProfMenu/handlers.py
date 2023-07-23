import re

import sqlalchemy
from aiogram.types import Message
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from Conexiune.db.tables.tables import ProfAdjust
from Conexiune.dialogs.standart_user.ProfMenu.states import ProfMenuSG


async def name_handler(m: Message, MessageInput, manager: DialogManager):
    if re.match(r'^[А-Яа-я\s]{4,50}$', m.text):
        maker: async_sessionmaker[AsyncSession] = manager.middleware_data['session_maker']
        async with maker() as session:
            async with session.begin():
                u = manager.dialog_data['u']
                # understand how to deal up without slct
                slct = sqlalchemy.select(ProfAdjust).filter(ProfAdjust.user_id == u.id)
                raw_p = await session.scalars(slct)
                p = raw_p.one()
                if not p.name:
                    p.name = m.text
                else:
                    p.name = m.text

        await manager.switch_to(ProfMenuSG.main)
    else:
        await m.reply('Имя не подходит. Используй только русские буквы')
