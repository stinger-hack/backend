import asyncio
from typing import AsyncGenerator, Optional
from aiohttp.web import Application
from aioredis import Redis as AioRedis, create_redis_pool

import settings


class Redis:
    """
        Service to work with redis
    """
    _client: Optional[AioRedis] = None

    @classmethod
    async def _connect(cls) -> None:
        """
        If _client class attribute isn't set, sets new connection
        :return:
        """
        if not cls._client:
            cls._client = await create_redis_pool(settings.REDIS_CONNECTION_STRING, loop=asyncio.get_event_loop())

    @classmethod
    async def close(cls) -> None:
        """
        Close seted connection and drop _client class attribute
        :return:
        """
        if cls._client is not None:
            cls._client.close()
            await cls._client.wait_closed()
            cls._client = None

    @classmethod
    async def get_client(cls) -> AioRedis:
        """
        Returns current redis connection
        :return: AioRedis
        """
        if not cls._client:
            await cls._connect()
        return cls._client


async def get_client() -> AioRedis:
    """

    :return:
    """
    return await Redis.get_client()


async def service(app: Application) -> AsyncGenerator:
    """

    :param app:
    :return:
    """
    app['redis'] = await Redis.get_client()
    yield
    await Redis.close()


__all__ = [
    'service',
    'get_client',
    'Redis'
]