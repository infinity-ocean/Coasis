""" This file represents configurations from files and environment"""
import logging
from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

@dataclass
class DatabaseConfig:
    """Database connection variables"""

    name: str = getenv("POSTGRES_DATABASE")
    user: str = getenv("POSTGRES_USER", "docker")
    passwd: str = getenv("POSTGRES_PASSWORD", None)
    port: int = int(getenv("POSTGRES_PORT", 5432))
    host: str = getenv("POSTGRES_HOST", "database")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def build_connection_str(self) -> str:
        """
        This function build a connection string
        """
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class RedisConfig:
    """Redis connection variables"""

    db: str = int(getenv("REDIS_DATABASE", 1))
    host: str = getenv("REDIS_HOST", "redis")
    port: int = int(getenv("REDIS_PORT", 6379))
    passwd: int = getenv("REDIS_PASSWORD")
    username: int = getenv("REDIS_USERNAME")
    state_ttl: int = getenv("REDIS_TTL_STATE", None)
    data_ttl: int = getenv("REDIS_TTL_DATA", None)


@dataclass
class BotConfig:
    """Bot configuration"""

    token: str = getenv("BOT_TOKEN")


@dataclass
class Configuration:
    """All in one configuration's class"""

    logging_level = int(getenv("LOGGING_LEVEL", logging.INFO))

    db = DatabaseConfig()
    redis = RedisConfig()
    bot = BotConfig()
