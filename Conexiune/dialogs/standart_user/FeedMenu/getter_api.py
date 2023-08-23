from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.prof_adjust import ProfAdjust


async def less_4h(added_time):
    elapsed_time = datetime.now() - added_time
    return elapsed_time <= timedelta(hours=4)


async def get_profiles(
        session: AsyncSession,
        min_age=18,
        max_age=60,
        sex=None,
        offset=0
):
    async with session.begin():
        if sex:
            slct = select(ProfAdjust).filter(
                ProfAdjust.age >= min_age,
                ProfAdjust.age <= max_age,
                ProfAdjust.sex == sex).\
                limit(20).offset(offset*20)
        elif not sex:
            slct = select(ProfAdjust).filter(
                ProfAdjust.age >= min_age,
                ProfAdjust.age <= max_age
            ).limit(20).offset(offset*20)
        raw_u = await session.scalars(slct)
        u_list = raw_u.all()
        return u_list
