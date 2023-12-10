from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Conexiune.database.tables.user import User
from database.tables.feed_settings import FeedSettings
from database.tables.prof_adjust import ProfAdjust


async def select_u(session: AsyncSession, tg_id: int, user_with: str):
    async with session.begin():
        if user_with == 'ProfAdjust':
            slct = select(User).where(User.tg_id == tg_id).options(selectinload(User.prof_adj))
        if user_with == 'FeedSettings':
            slct = select(User).where(User.tg_id == tg_id).options(selectinload(User.feed_setts))
        u = (await session.scalars(slct)).one_or_none()
        return u


async def fill_front(p):
    front = {'one_exists': True}
    if p.photo:
        front['photo'] = MediaAttachment(ContentType.PHOTO, file_id=MediaId(p.photo))
    if p.name:
        front['name'] = p.name
    if p.age:
        front['age'] = p.age
    if p.sex:
        front['sex'] = p.sex
    if p.location:
        front['location'] = p.location
    if p.descr:
        front['descr'] = p.descr
    return front


async def handle_back(p, back):
    if 'u_id' not in back:
        back['u_id'] = p.user_fk
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
