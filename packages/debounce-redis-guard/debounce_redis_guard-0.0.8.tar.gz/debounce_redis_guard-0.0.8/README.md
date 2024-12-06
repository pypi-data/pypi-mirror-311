# debounce-redis-guard

debounce-redis-guard is a Python library designed to handle debouncing of requests in applications that support multiple workers. This library helps to prevent multiple identical requests from being processed simultaneously, thus improving efficiency and reducing redundant processing.

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

from debounce_redis_guard import Debouncer, RedisConfig

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

## Implementation Behavior with Concurrent clone request with ApiDebouncer: Sequence Diagram
![Screenshot](https://raw.githubusercontent.com/cdeepana/debounce_redis_guard/refs/heads/main/concurrent_clone_request.png)


## Implementation Behavior with  clone requests (time to time - within TTL duration) with ApiDebouncer: Sequence Diagram

[//]: # (![Screenshot]&#40;docs/images/delayed_clone_request.png&#41;)
![Screenshot](https://raw.githubusercontent.com/cdeepana/debounce_redis_guard/refs/heads/main/delayed_clone_request.png)


## Jmeter Summary Report Sample to Compair with and without debouncing feature

[//]: # (![Screenshot]&#40;docs/images/experiment.png&#41;)
![Screenshot](https://raw.githubusercontent.com/cdeepana/debounce_redis_guard/refs/heads/main/experiment.png)








