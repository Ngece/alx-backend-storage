#!/usr/bin/env python3
""" Module for using redis in Python """

import redis
from functools import wraps
import requests
from typing import Callable


cache = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to count number of times functions are called"""
    @wraps(method)
    def count_calls_wrapper(*args) -> str:
        """Counts number of calls wrapped function makes"""
        key = f"count:{args[0]}"
        cache.incr(key)
        cache.setex('count', 10, cache.get(key))
        return method(*args)

    return count_calls_wrapper


@count_calls
def get_page(url: str) -> str:
    """GET HTML content from URL and return it"""
    r = requests.get(url)

    return r.text