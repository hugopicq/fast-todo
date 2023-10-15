import contextlib
import logging
import asyncpg

from fast_todo.app.config import config

logger = logging.getLogger("uvicorn")

class PGPool:
    """
    Postgresql connection pool convenience class.
    """

    _pool: asyncpg.Pool | None = None

    @classmethod
    async def get_pool(cls) -> asyncpg.Pool | None:
        """
        Get a postgres connection pool.
        """
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                dsn=config.postgres_dsn,
                min_size=config.asyncpg_min_pool_size,
                max_size=config.asyncpg_max_pool_size,
                max_inactive_connection_lifetime=300,
                command_timeout=300,
                server_settings={
                    "jit": "off"
                },
            )

        return cls._pool

    @classmethod
    @contextlib.asynccontextmanager
    async def get_connection(cls):
        """
        Get a connection from the connection pool.
        """
        pool = await cls.get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                yield conn

    @classmethod
    async def close_connection(cls):
        """
        Close the connection pool.
        """
        if cls._pool is not None:
            logger.info("Closing connection pool")
            await cls._pool.close()
        else:
            logger.info("Connection pool already closed")
