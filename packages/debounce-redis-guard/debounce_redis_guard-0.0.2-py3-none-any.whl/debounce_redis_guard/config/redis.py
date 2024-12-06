# MIT License
# Copyright (c) 2024 chathura deepana  ( cdeepana )
# See the LICENSE file for details.


import json
import asyncio
from redis.asyncio import Redis
from redis import Redis as Redis_Sync
from aiocache import caches
from cryptography.fernet import Fernet

# Generated key and instantiate a Fernet instance
cipher_suite = Fernet('7xsz27fnp-K0RoMq4bFtkgJuggDaSu1O51AAqD1fawI=')


def encrypt_data(data: str) -> bytes:
    """Encrypts data."""
    return cipher_suite.encrypt(data.encode())


def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypts data."""
    return cipher_suite.decrypt(encrypted_data).decode()


class RedisInstance:
    _instance = None

    def __init__(self):
        self._initialized = None
        self.response_cache = None
        print('Redis Instance running')
        self.redisX = None
        self.redisXSync = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisInstance, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    async def initialize_redis(self, redis_connection_string:str):
        if not self._initialized:
            try:
                self.redisX = await Redis.from_url(redis_connection_string)
                # self.redisX = await Redis.from_url('redis://default:AI64W7Z6K0@localhost:6379/10')
                await self.redisX.ping()
                self.redisXSync = Redis_Sync.from_url(redis_connection_string)

                caches.set_config({
                    'default': {
                        'cache': 'aiocache.RedisCache',
                        'endpoint': '127.0.0.1',
                        'port': 6379,
                        'db': 10,
                        'serializer': {
                            'class': 'aiocache.serializers.JsonSerializer'
                        },
                        'namespace': 'main'
                    }
                })
                self.response_cache = caches.get('default')

                self._initialized = True
            except Exception as e:
                raise RuntimeError(f"{repr(e)}")

    async def get_redis(self, key):
        value = await self.redisX.get(key)
        if value:
            return json.loads(decrypt_data(value))  # Deserialize JSON string to dict
        return None


    async def set_redis(self, key, value, ex=60):
        if isinstance(value, dict):
            value = json.dumps(value)
        value = encrypt_data(value)
        # print("key",key, "value",value)
        await self.redisX.set(key, value, ex=ex)


    async def set_lock(self, request_hash: str, value: str, ex=50):
        await self.redisX.set(request_hash, value, ex=ex)


    async def get_lock(self, request_hash: str):
        return await self.redisX.get(request_hash)


    async def delete_lock(self, request_hash: str):
        await self.redisX.delete(request_hash)


    async def set_event(self, request_hash: str, ex=50):
        await self.redisX.set(request_hash, 'set', ex=ex)


    async def wait_for_event(self, request_hash: str):
        while True:
            event_status = await self.redisX.get(request_hash)
            if event_status == b'set':
                break
            await asyncio.sleep(1)  # Wait before checking again


# Instantiate the singleton RedisInstance and initialize Redis
redisInstance = RedisInstance()


