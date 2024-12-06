# MIT License
# Copyright (c) 2024 chathura deepana  ( cdeepana )
# See the LICENSE file for details.


import hashlib
import json
import logging
import asyncio

from starlette.responses import JSONResponse
from functools import wraps
from decimal import Decimal
from datetime import datetime
from ..common import  CommonResponse,RedisConfig
from ..config import redisInstance


def generate_request_hash(body: dict = None, function_name: str = ""):
    """
    Generate a hash for the request based on the body and function name to identify unique requests.
    """
    hash_input = f"{body}:{function_name}"
    return hashlib.sha256(hash_input.encode()).hexdigest()


class Debouncer:
    _instance = None
    _initialized = False

    def __new__(cls, logger=None, redis_config : RedisConfig =None):
        if cls._instance is None:
            cls._instance = super(Debouncer, cls).__new__(cls)
            cls._instance._init(logger,redis_config)
        return cls._instance


    def _init(self, logger=None, redis_config=None):
        if not self._initialized:
            if logger:
                self.logger = logger
                self.logger.info('third party logger attached . . .')
            else:
                # Default logger if no logger is passed
                self.logger = logging.getLogger(__name__)
                self.logger.info('default logger created . . .')

            try:
                self.lock_cache_key_prefix = 'lock:'
                self.event_cache_key_prefix = 'event:'
                self._redis_connection_string = f"redis://{redis_config.username}:{redis_config.password}@{redis_config.host}:{redis_config.port}/{redis_config.db}"
                self._initialized = True
            except Exception as e:
                self.logger.error('RedisConfig Error . . .')


    def debounce(self, ttl=60, function_name=None, identity_name='data'):
        """
        Decorator to debounce requests.
        """

        def custom_serializer(obj):
            if isinstance(obj, Decimal):
                return float(obj)  # or str(obj) if you prefer string representation
            elif isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")

        def decorator(func):

            @wraps(func)
            async def wrapper(*args, **kwargs):
                await redisInstance.initialize_redis(self._redis_connection_string)
                try:
                    async def handle_request():
                        data: dict = kwargs.get(identity_name, {})
                        request_hash = generate_request_hash(data, function_name)

                        if not await redisInstance.get_lock(self.lock_cache_key_prefix + request_hash):
                            # Get the cached response
                            cached_response = await redisInstance.get_redis(request_hash)
                            if cached_response:
                                self.logger.info(
                                     f"::: ( non-lock state ) Request debounce detected on function : {function_name} :::\n\t| request : {data} |")
                                # validated_response = CommonResponse(**(json.loads(cached_response['content']))).dict()
                                cached_response_content = cached_response['content']
                                validated_response = json.loads(cached_response_content)

                                response = JSONResponse(content=validated_response,
                                                        status_code=cached_response['status_code'])
                                return response
                            else:
                                # set lock
                                await redisInstance.set_lock(self.lock_cache_key_prefix + request_hash, 'locked', 15)
                                # Process the request
                                response = await asyncio.create_task(func(*args, **kwargs))
                                response_data = {}
                                if isinstance(response, dict):
                                    response_data = {
                                        'content': json.dumps(response, default=custom_serializer),
                                        'status_code': 200
                                    }
                                elif isinstance(response, JSONResponse):
                                    response_data = {
                                        'content': response.body.decode('utf-8'),
                                        'status_code': response.status_code
                                    }
                                await redisInstance.set_redis(request_hash, json.dumps(response_data, default=custom_serializer), ttl)
                                # Release the lock
                                await redisInstance.delete_lock(self.lock_cache_key_prefix + request_hash)
                                # Set event to notify other waiting processes
                                await redisInstance.set_event(self.event_cache_key_prefix + request_hash, ttl - 1)

                                # Return the response
                                return response
                        else:
                            # Wait for the event to be set
                            await redisInstance.wait_for_event(self.event_cache_key_prefix + request_hash)
                            # Get the cached response
                            cached_response = await redisInstance.get_redis(request_hash)
                            if cached_response:
                                self.logger.info(
                                    f"::: ( lock state ) Request debounce detected on function : {function_name} :::\n\t| request : {data} |")
                                # validated_response = CommonResponse(**(json.loads(cached_response['content']))).dict()

                                cached_response_content = cached_response['content']
                                validated_response = json.loads(cached_response_content)


                                response = JSONResponse(content=validated_response,
                                                        status_code=cached_response['status_code'])
                                return response

                    # Create and run the task for handling the request
                    return await asyncio.create_task(handle_request())

                except Exception as e:
                    self.logger.error(
                         f"::: Request debounce error detected on {function_name} :::\n\t| request : ( debounce error ){e} |")

            return wrapper

        return decorator