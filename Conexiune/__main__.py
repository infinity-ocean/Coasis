import asyncio

from aiogram import Bot
from aiogram.filters import CommandStart
from aiogram_dialog import setup_dialogs

import sys
import os
sys.path.append(os.path.join(sys.path[0], '..'))
from config import Configuration
from database.infrastructure import create_engine, create_session_maker
from database.tables.base import Base
from handlers.start import start
from middlewares.sess_reg_role import db_middleware
from api import setup_dispatcher
from dialogs.standart_user.FeedMenu.dialog import feed_dialog
from dialogs.standart_user.ProfMenu.dialog import prof_dialog
from dialogs.standart_user.menu_dialog import main_menu


# logger = logging.getLogger(__name__)


async def start_bot():
    #### inf
    conf = Configuration()
    # logging.basicConfig(level=conf.logging_level,
    #                     format="%(name)s - %(message)s")
    # logger.error("Starting bot...")
    #### database
    engine = create_engine(conf.db.build_connection_str())
    maker = create_session_maker(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    #### bot
    bot = Bot(conf.bot.token)
    dp, redis = setup_dispatcher()
    dp.message.register(start, CommandStart())
    #### mdw
    dp.message.middleware(db_middleware())
    dp.callback_query.middleware(db_middleware())
    #### dialogs
    dp.include_routers(main_menu, prof_dialog, feed_dialog)
    setup_dialogs(dp)
    await dp.start_polling(bot, maker=maker, redis=redis)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except(KeyboardInterrupt, SystemExit):
        ...
        # logger.error("Bot stopped!")
