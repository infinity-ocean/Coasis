import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram_dialog import setup_dialogs

from Conexiune.config import Configuration
from Conexiune.db.infrastructure import create_engine, create_session_maker
from Conexiune.db.tables.base import Base
from Conexiune.dialogs.standart_user.ProfMenu.dialog import prof_dialog
from Conexiune.middlewares.registration import RegistrationMiddleware
from Conexiune.handlers.start import start

logger = logging.getLogger(__name__)


async def start_bot():
    #### inf
    conf = Configuration()
    logging.basicConfig(level=conf.logging_level,
                        format="%(name)s - %(message)s")
    logger.error("Starting bot...")
    #### db
    engine = create_engine(conf.db.build_connection_str())
    session_maker = create_session_maker(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    #### bot
    bot = Bot(conf.bot.token)
    dp = Dispatcher()
    dp.message.register(start, CommandStart())
    #### mdw
    dp.message.middleware.register(RegistrationMiddleware())
    dp.callback_query.middleware.register(RegistrationMiddleware())
    #### dialogs
    dp.include_router(prof_dialog)
    setup_dialogs(dp)
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except(KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
