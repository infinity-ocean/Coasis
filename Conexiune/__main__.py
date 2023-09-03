import asyncio

from aiogram import Bot
from aiogram.filters import CommandStart
from aiogram_dialog import setup_dialogs

from Conexiune.config import Configuration
from Conexiune.database.infrastructure import create_engine, create_session_maker
from Conexiune.database.tables.base import Base
from Conexiune.dialogs.standart_user.ProfMenu.dialog import prof_dialog
from Conexiune.handlers.start import start
from Conexiune.middlewares.registration import db_middleware
from api import setup_dispatcher
from dialogs.standart_user.FeedMenu.dialog import feed_dialog


# logger = logging.getLogger(__name__)


async def start_bot():
    print('play')
    #### inf
    conf = Configuration()
    # logging.basicConfig(level=conf.logging_level,
    #                     format="%(name)s - %(message)s")
    # logger.error("Starting bot...")
    #### database
    engine = create_engine(conf.db.build_connection_str())
    maker = create_session_maker(engine)
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    #### bot
    bot = Bot(conf.bot.token)
    dp = setup_dispatcher()
    dp.message.register(start, CommandStart())
    #### mdw
    dp.message.middleware(db_middleware())
    dp.callback_query.middleware(db_middleware())
    #### dialogs
    dp.include_routers(prof_dialog, feed_dialog)
    setup_dialogs(dp)
    await dp.start_polling(bot, maker=maker)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except(KeyboardInterrupt, SystemExit):
        ...
        # logger.error("Bot stopped!")
