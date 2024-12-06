# debounce-redis-guard

DebounceMaster is a Python library designed to handle debouncing of requests in applications that support multiple workers. This library helps to prevent multiple identical requests from being processed simultaneously, thus improving efficiency and reducing redundant processing.

## Features

- Debounce requests to avoid duplicate processing
- Supports multiple workers
- Integration with Redis for distributed locking and caching
- Custom logging

## Installation

```bash
pip install debounce-redis-guard
```




# Initialize Debouncer with logger and Redis configuration

```

from debounce-redis-guard import Debouncer, RedisConfig

debouncer = Debouncer(logger=my_logger, redis_config=my_redis_config)

```


## Usage

```
@debouncer.debounce(ttl=60, function_name='my_function', identity_name='data')
async def my_function(data):
    # Your function logic here
    return {'message': 'Processed'}
    
```

## Example Usage

```
@router.get("/perform-final-payment", , name="final payment perform by users - should only call one time.")
@debouncer.debounce(ttl=599, function_name="getAllPaymentGatewayList")
async def finalPay():

    response = code functionality
    return response

```





