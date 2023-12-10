from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio.client import Redis


def setup_dispatcher():
    redis = Redis()
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dp = Dispatcher(storage=storage)
    return dp
