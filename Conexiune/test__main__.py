import asyncio
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine, AsyncEngine

from Conexiune.config import Configuration
from sqlalchemy import text

def create_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


def create_session_maker(engine: AsyncEngine = None) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def main():
        conf = Configuration()
        engine = create_async_engine(
            url=conf.db.build_connection_str(), echo=True, pool_pre_ping=True)
        session_maker = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
        session_maker = create_session_maker(engine)

        async with session_maker.begin() as conn:
                conn.add()


asyncio.run(main())



