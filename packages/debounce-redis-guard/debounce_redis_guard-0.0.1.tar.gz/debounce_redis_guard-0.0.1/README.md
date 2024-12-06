# debounce_redis_guard

DebounceMaster is a Python library designed to handle debouncing of requests in applications that support multiple workers. This library helps to prevent multiple identical requests from being processed simultaneously, thus improving efficiency and reducing redundant processing.

## Features

- Debounce requests to avoid duplicate processing
- Supports multiple workers
- Integration with Redis for distributed locking and caching
- Custom logging

## Installation

```bash
pip install debounce_redis_guard