from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.prof_adjust import ProfAdjust


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
            slct = slct.offset(offset*20)
        raw_u = await session.scalars(slct)
        u_list = raw_u.all()
        return u_list
