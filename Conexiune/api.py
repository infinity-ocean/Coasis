from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio.client import Redis


def setup_dispatcher():
    storage = RedisStorage(
        redis=Redis(),
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dp = Dispatcher(storage=storage)
    return dp
