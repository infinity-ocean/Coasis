import asyncio
import logging

from aiogram import Bot, Dispatcher

from Conexiune.config import Configuration
from trsh.TrashBin.bot.handlers.handlers import router


async def main():
    conf = Configuration()
    bot = Bot(conf.bot.token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
