import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from Conexiune.config import Configuration
from Conexiune.db.infrastructure import create_engine, create_session_maker
from Conexiune.db.tables.base import Base
from Conexiune.db.tables.tables import User


async def test():
    conf = Configuration()
    engine = create_engine(conf.db.build_connection_str())
    session_maker = create_session_maker(engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        async with session.begin():
            # check prof_adj values
            # stmt = select(ProfAdjust.name, ProfAdjust.descr).select_from(User).join(User.prof_adj).where(User.tg_id == 301715373)
            # stmt2 = select(ProfAdjust.name, ProfAdjust.descr).join_from(User, ProfAdjust).where(User.tg_id == 301715373)
            stmt3 = select(User).options(selectinload(User.prof_adj)).filter(User.tg_id == 301715373)
            result_u_profadj = await session.scalars(stmt3)
            res = result_u_profadj.one()

asyncio.run(test())
