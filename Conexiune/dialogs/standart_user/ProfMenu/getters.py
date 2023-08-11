from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Conexiune.database.tables.tables import User, ProfAdjust


async def mw_getter(**kwargs):
    session: AsyncSession = kwargs['session']
    event = kwargs['event_from_user']
    manager = kwargs['dialog_manager']
    async with session.begin():
        slct = select(User).where(User.tg_id == event.id).options(selectinload(User.prof_adj))
        raw_u = await session.scalars(slct)
        u = raw_u.one_or_none()
        if not u:
            slct_u_reg = User(tg_id=event.id, username=event.username, first_name=event.first_name)
            slct_u_reg.prof_adj = ProfAdjust()
            await session.merge(slct_u_reg)
            slct_u_new = select(User).where(User.tg_id == event.id).options(selectinload(User.prof_adj))
            _u_new = await session.scalars(slct_u_new)
            u_new = _u_new.one_or_none()
            manager.dialog_data['u'] = u_new
            return {'fresh_created': True}
    manager.dialog_data['u'] = u
    p = u.prof_adj
    if not p.photo and not p.name and not p.age and not p.sex and not p.location and not p.descr:
        return {'not_filled': True}
    else:
        widget_filler = {'at_least_one': True}
        if p.photo:
            widget_filler['photo'] = MediaAttachment(ContentType.PHOTO, file_id=MediaId(p.photo))
            widget_filler['1_photo'] = True
        elif not p.photo:
            widget_filler['photo_text'] = '🟡 Ты пока не заполнил фото'
            widget_filler['0_photo'] = True
        if p.name:
            widget_filler['name'] = f'🟢 Твоё имя - {p.name}'
        elif not p.name:
            widget_filler['name'] = '🟡 Ты пока не заполнил имени'
        if p.age:
            widget_filler['age'] = f'🟢 Твой возраст - {p.age}'
        elif not p.age:
            widget_filler['age'] = '🟡 Ты пока не заполнил возраст'
        if p.sex:
            widget_filler['sex'] = f'🟢 Твой пол - {p.sex}'
        elif not p.sex:
            widget_filler['sex'] = '🟡 Ты пока не заполнил свой пол'
        if p.latitude:
            widget_filler['loc'] = f'🟢 Твоя локация - {p.location}'
        elif not p.latitude:
            widget_filler['loc'] = f'🟡 Ты пока не заполнил свою локацию'
        if p.descr:
            widget_filler['descr'] = f'🟢 Твоё описание - {p.descr}'
        elif not p.descr:
            widget_filler['descr'] = '🟡 Ты пока не заполнил описание'
        return widget_filler


async def pw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    if not u:
        return {'0_photo': True}
    elif not u.prof_adj:
        return {'0_photo': True}
    elif not u.prof_adj.photo:
        return {'0_photo': True}
    elif u.prof_adj.photo:
        image = MediaAttachment(
            ContentType.PHOTO, file_id=MediaId(u.prof_adj.photo)
        )
        return {'1_photo': True, 'photo': image}


async def nw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    if not u:
        return {'0_name': True}
    elif not u.prof_adj:
        return {'0_name': True}
    elif not u.prof_adj.name:
        return {'0_name': True}
    elif u.prof_adj.name:
        return {'1_name': True, 'name': u.prof_adj.name}


async def aw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    if not u:
        return {'0_age': True}
    elif not u.prof_adj:
        return {'0_age': True}
    elif not u.prof_adj.age:
        return {'0_age': True}
    elif u.prof_adj.age:
        return {'1_age': True, 'age': u.prof_adj.age}


async def sw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    if not u:
        return {'0_sex': True}
    elif not u.prof_adj:
        return {'0_sex': True}
    elif not u.prof_adj.sex:
        return {'0_sex': True}
    elif u.prof_adj.sex:
        return {'1_sex': True, 'sex': u.prof_adj.sex}


async def lw_getter(**kwargs):
    u = kwargs['dialog_manager'].dialog_data['u']
    if not u:
        return {'0_loc': True}
    elif not u.prof_adj:
        return {'0_loc': True}
    elif not u.prof_adj.location:
        return {'0_loc': True}
    elif u.prof_adj.location:
        return {'1_loc': True, 'loc': u.prof_adj.location}


async def dw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    if not u:
        return {'0_descr': True}
    elif not u.prof_adj:
        return {'0_descr': True}
    elif not u.prof_adj.descr:
        return {'0_descr': True}
    elif u.prof_adj.descr:
        return {'1_descr': True, 'descr': u.prof_adj.descr}
