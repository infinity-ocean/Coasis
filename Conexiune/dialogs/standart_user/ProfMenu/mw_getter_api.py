from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Conexiune.database.tables.tables import User, ProfAdjust


async def select_u(session: AsyncSession, tg_id: int):
    async with session.begin():
        slct = select(User).where(User.tg_id == tg_id).options(selectinload(User.prof_adj))
        raw_u = await session.scalars(slct)
        u = raw_u.one_or_none()
        return u


async def registrate_u(session: AsyncSession, event, back):
    async with session.begin():
        u_reg = User(tg_id=event.id, username=event.username, first_name=event.first_name)
        u_reg.prof_adj = ProfAdjust()
        await session.merge(u_reg)
        slct_u_fresh = select(User).where(User.tg_id == event.id).options(selectinload(User.prof_adj))
        _u_fresh = await session.scalars(slct_u_fresh)
        u_fresh = _u_fresh.one_or_none()
        back['u_id'] = u_fresh.id
        return u_fresh


async def fill_front(p):
    if not p.photo and not p.name and not p.age and not p.sex and not p.location and not p.descr:
        return {'not_filled': True}
    front = {'one_exists': True}
    if p.photo:
        front['photo'] = MediaAttachment(ContentType.PHOTO, file_id=MediaId(p.photo))
    else:
        front['0_photo'] = True
    if p.name:
        front['name'] = p.name
    else:
        front['0_name'] = True
    if p.age:
        front['age'] = p.age
    else:
        front['0_age'] = True
    if p.sex:
        front['sex'] = p.sex
    else:
        front['0_sex'] = True
    if p.location:
        front['location'] = p.location
    else:
        front['0_location'] = True
    if p.descr:
        front['descr'] = p.descr
    else:
        front['0_descr'] = True
    return front


async def handle_back(p, back):
    if 'u_id' not in back:
        back['u_id'] = p.user_id
    # ----------------------------------------------------------------------------- #
    if p.photo:
        back['photo'] = p.photo
    else:
        if 'photo' in back: del back['photo']
    if p.name:
        back['name'] = p.name
    else:
        if 'name' in back: del back['name']
    if p.age:
        back['age'] = p.age
    else:
        if 'age' in back: del back['age']
    if p.sex:
        back['sex'] = p.sex
    else:
        if 'sex' in back: del back['sex']
    if p.location:
        back['location'] = p.location
    else:
        if 'location' in back: del back['location']
    if p.descr:
        back['descr'] = p.descr
    else:
        if 'descr' in back: del back['descr']
