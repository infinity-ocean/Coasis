from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.feed_settings import FeedSettings
from dialogs.standart_user.FeedMenu.states import FeedSG


async def set_m_setts(callback: CallbackQuery, button: Button,
                      manager: DialogManager):
    session: AsyncSession = manager.middleware_data['session']

    async with session.begin():
        _id = manager.dialog_data['u_id']
        upd = update(FeedSettings).values(sex='М').filter(FeedSettings.user_fk == _id)
        await session.execute(upd)
    await manager.switch_to(FeedSG.settings)


async def set_w_setts(callback: CallbackQuery, button: Button,
                      manager: DialogManager):
    session: AsyncSession = manager.middleware_data['session']
    async with session.begin():
        _id = manager.dialog_data['u_id']
        upd = update(FeedSettings).values(sex='Ж').filter(FeedSettings.user_fk == _id)
        await session.execute(upd)
    await manager.switch_to(FeedSG.settings)


async def clear_sex_setts(callback: CallbackQuery, button: Button,
                          manager: DialogManager):
    session: AsyncSession = manager.middleware_data['session']
    async with session.begin():
        _id = manager.dialog_data['u_id']
        exp = update(FeedSettings).values(sex=None).filter(FeedSettings.user_fk == _id)
        await session.execute(exp)
    await manager.switch_to(FeedSG.settings)
