from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.feed_settings import FeedSettings
from database.tables.prof_adjust import ProfAdjust


async def get_setts(
        session: AsyncSession,
        u_id: int) -> dict:
    async with session.begin():
        _fs = await session.scalar(
            select(FeedSettings).filter(FeedSettings.user_fk == u_id)
        )
        fs = {}
        if _fs.sex:
            fs['sex'] = _fs.sex
        if _fs.min_age:
            fs['min_age'] = _fs.min_age
        if _fs.max_age:
            fs['max_age'] = _fs.max_age
        if _fs.location:
            fs['location'] = _fs.location
        return fs


async def get_profiles(
        session: AsyncSession,
        min_age=18,
        max_age=60,
        sex: str = None,
        offset=0
):
    async with session.begin():
        slct = select(ProfAdjust).filter(
            ProfAdjust.age >= min_age,
            ProfAdjust.age <= max_age).limit(20)
        if sex:
            slct = slct.filter(ProfAdjust.sex == sex)
        if offset:
            slct = slct.offset(offset * 20)
        u_list = (await session.scalars(slct)).all()
        return u_list
