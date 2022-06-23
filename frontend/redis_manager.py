#!/usr/bin/env python3
import aioredis
from json import loads as loadJSON, JSONDecodeError


class RedisManager:

    def __init__(self, redis_url):
        self.redis_url = redis_url

    async def request(self, prefix: str, keys: list, response_editor):
        instance = aioredis.from_url(self.redis_url)
        responses = await instance.mget(f"{prefix}.{key}" for key in keys)

        try:
            result = response_editor([loadJSON(resp) for resp in responses])
        except JSONDecodeError as e:
            # TODO manage JSONDecodeError
            raise e
        return result
