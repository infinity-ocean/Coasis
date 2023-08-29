import re

from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from Conexiune.dialogs.standart_user.ProfMenu.states import ProfSG
from database.tables.prof_adjust import ProfAdjust
from dialogs.standart_user.ProfMenu.location_api import coords_to_location


#### PW BLOCK
async def photo_handler(m: Message, MessageInput, manager: DialogManager):
    session: AsyncSession = manager.middleware_data['session']
    async with session.begin():
        _id = manager.dialog_data['u_id']
        upd = update(ProfAdjust).values(photo=m.photo[-1].file_id).filter(ProfAdjust.user_id == _id)
        await session.execute(upd)
    await manager.switch_to(ProfSG.main)


#### NW BLOCK
async def name_handler(m: Message, MessageInput, manager: DialogManager):
    if re.match(r'^[А-Яа-я\s]{4,50}$', m.text):
        session: AsyncSession = manager.middleware_data['session']
        async with session.begin():
            _id = manager.dialog_data['u_id']
            upd = update(ProfAdjust).values(name=m.text).filter(ProfAdjust.user_id == _id)
            await session.execute(upd)
        await manager.switch_to(ProfSG.main)
    else:
        await m.reply('Имя не подходит. Используй только русские буквы')


#### AW BLOCK
async def age_handler(m: Message, MessageInput, manager: DialogManager):
    if re.match(r'^(1[89]|[2-5][0-9]|60)$', m.text):
        session: AsyncSession = manager.middleware_data['session']
        async with session.begin():
            _id = manager.dialog_data['u_id']
            upd = update(ProfAdjust).values(age=int(m.text)).filter(ProfAdjust.user_id == _id)
            await session.execute(upd)
        await manager.switch_to(ProfSG.main)
    else:
        await m.reply('Неправильный возраст. Принимаются только цифры')


#### SW BLOCK
async def m_select(callback: CallbackQuery, button: Button,
                   manager: DialogManager):
    session: AsyncSession = manager.middleware_data['session']
    async with session.begin():
        _id = manager.dialog_data['u_id']
        upd = update(ProfAdjust).values(sex='М').filter(ProfAdjust.user_id == _id)
        await session.execute(upd)
    await manager.switch_to(ProfSG.main)


async def w_select(callback: CallbackQuery, button: Button,
                   manager: DialogManager):
    session: AsyncSession = manager.middleware_data['session']
    async with session.begin():
        _id = manager.dialog_data['u_id']
        upd = update(ProfAdjust).values(sex='Ж').filter(ProfAdjust.user_id == _id)
        await session.execute(upd)
    await manager.switch_to(ProfSG.main)


#### LW BLOCK
async def loc_handler(m: Message, MessageInput, manager: DialogManager):
    session: AsyncSession = manager.middleware_data['session']
    async with session.begin():
        _id = manager.dialog_data['u_id']
        l = m.location
        loc = await coords_to_location(l.latitude, l.longitude)
        upd = update(ProfAdjust).values(location=loc, latitude=l.latitude, longitude=l.longitude).filter(ProfAdjust.user_id == _id)
        await session.execute(upd)
    await m.chat.delete_message(manager.dialog_data['loc_msg_id']) # todo delete a list of messages instead of 1
    await manager.switch_to(ProfSG.main)


async def send_loc_kbd(callback: CallbackQuery, button: Button,
                       manager: DialogManager):
    kb = [[types.KeyboardButton(text="Скинуть локацию", request_location=True)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                         one_time_keyboard=True,
                                         resize_keyboard=True,
                                         input_field_placeholder='Жду локацию')
    msg = await callback.message.answer('...', reply_markup=keyboard)
    manager.dialog_data['loc_msg_id'] = msg.message_id


#### DW BLOCK
async def descr_handler(m: Message, MessageInput, manager: DialogManager):
    if re.match(r'^[А-Яа-я\s,.-]{10,520}$', m.text):
        session: AsyncSession = manager.middleware_data['session']
        async with session.begin():
            _id = manager.dialog_data['u_id']
            upd = update(ProfAdjust).values(descr=m.text).filter(ProfAdjust.user_id == _id)
            await session.execute(upd)
        await manager.switch_to(ProfSG.main)
    else:
        await m.reply('Описание не подходит. Используй только русские буквы')
