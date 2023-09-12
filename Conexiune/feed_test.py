import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import Configuration
from database.infrastructure import create_engine, create_session_maker
from database.tables.user import ProfAdjust


async def main():
    conf = Configuration()
    engine = create_engine(conf.db.build_connection_str())
    maker = create_session_maker(engine)
    async with maker() as session:
        result = await select_profiles(session, sex='М')
        print(result)

async def select_profiles(
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
                limit(20).offset(0+offset*20)
        elif not sex:
            slct = select(ProfAdjust).filter(
                ProfAdjust.age >= min_age,
                ProfAdjust.age <= max_age
            ).limit(20).offset(0+offset*20)
        raw_u = await session.scalars(slct)
        u = raw_u.all()
        return u



asyncio.run(main())
