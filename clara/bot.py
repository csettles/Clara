from discord.ext.commands import Bot
import aioredis
import uvloop
import asyncio

from clara.utils.logger import logger

class Clara(Bot):
    def __init__(self, *args, **kwargs):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        super().__init__(*args, **kwargs)
        self._redis = None

    async def _connect_redis(self):
        try:
            self._redis = await aioredis.create_redis(('localhost', 6379))
            logger.info('Connected to redis instance.')
            return self._redis
        except ConnectionRefusedError:
            logger.error('Failed to connect to redis instance.')
            logger.info('Shutting down bot...')
            await self.close()
            return

    async def get_redis(self):
        if self._redis is None:
            return await self._connect_redis()

        return self._redis

    async def logout(self):
        super().logout()

        # close the aiohttp ClientSession()
        # for some reason this isn't handled by discord.py
        await self.http.session.close()

        if self._redis is not None:
            self._redis.close()
            await self._redis.wait_closed()
            logger.info('Closed connection to the redis instance.')
