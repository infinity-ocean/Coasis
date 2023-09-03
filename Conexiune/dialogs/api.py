from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Conexiune.database.tables.user import User


async def to_file_id(photo: str):
    return MediaAttachment(ContentType.PHOTO, file_id=MediaId(photo))


async def get_u_id(session: AsyncSession, tg_id, data):
    async with session.begin():
        u_id = await session.scalar(
            select(User.id).filter(User.tg_id == tg_id)
        )
        data['u_id'] = u_id
        return u_id
