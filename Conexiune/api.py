from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio.client import Redis


def setup_dispatcher():
    redis = Redis()
    dp = Dispatcher(storage=RedisStorage(redis, DefaultKeyBuilder(with_destiny=True)))
    return dp
