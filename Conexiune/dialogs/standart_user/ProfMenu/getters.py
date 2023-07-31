from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Conexiune.db.tables.tables import User, ProfAdjust


async def mw_getter(**kwargs):
    session: AsyncSession = kwargs['session']
    event = kwargs['event_from_user']
    manager = kwargs['dialog_manager']
    async with session.begin():
        slct = select(User).where(User.tg_id == event.id).options(selectinload(User.prof_adj))
        raw_u = await session.scalars(slct)
        u = raw_u.one()
        '''user with connected profadj'''
        # return stat-stat-dyn
        if not u.prof_adj:
            # inserting empty ProfAdjust linked to user creation
            await session.merge(ProfAdjust(user_id=u.id))
            manager.dialog_data['u'] = u
            return {'fresh_created': True}
        p = u.prof_adj
        manager.dialog_data['u'] = u
    if not p.photo and not p.name and not p.age and not p.descr and not p.sex:  # todo + ----l-
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
        if p.descr:
            widget_filler['descr'] = f'🟢 Твоё описание - {p.descr}'
        elif not p.descr:
            widget_filler['descr'] = '🟡 Ты пока не заполнил описание'
        return widget_filler


async def pw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    if not u.prof_adj:
        return {'0_photo': True}
    elif not u.prof_adj.photo:
        return {'0_photo': True}
    else:
        image = MediaAttachment(
            ContentType.PHOTO, file_id=MediaId(u.prof_adj.photo)
        )
        return {'1_photo': True, 'photo': image}


async def nw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    if not u.prof_adj:
        return {'0_name': True}
    elif not u.prof_adj.name:
        return {'0_name': True}
    else:
        return {'1_name': True, 'name': u.prof_adj.name}


async def aw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    if not u.prof_adj:
        return {'0_age': True}
    elif not u.prof_adj.age:
        return {'0_age': True}
    else:
        return {'1_age': True, 'age': u.prof_adj.age}

async def sw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    if not u.prof_adj:
        return {'0_sex': True}
    elif not u.prof_adj.sex:
        return {'0_sex': True}
    else:
        return {'1_sex': True, 'sex': u.prof_adj.sex}


async def dw_getter(**kwargs):
    manager = kwargs['dialog_manager']
    u = manager.dialog_data['u']
    if not u.prof_adj:
        return {'0_descr': True}
    elif not u.prof_adj.descr:
        return {'0_descr': True}
    else:
        return {'1_descr': True, 'descr': u.prof_adj.descr}
