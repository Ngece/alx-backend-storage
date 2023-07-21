#!/usr/bin/env python3
""" Module for using redis in Python """

import redis
from functools import wraps
import requests
from typing import Callable

cache = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times functions are called"""
    @wraps(method)
    def count_calls_wrapper(*args) -> str:
        """Counts the number of calls the wrapped function makes"""
        key = f"count:{args[0]}"
        cache.incr(key)
        cache.expire(key, 10)
        return method(*args)

    return count_calls_wrapper


@count_calls
def get_page(url: str) -> str:
    """GET HTML content from URL and return it"""
    r = requests.get(url)
    return r.text


# Test the function with a slow response URL
if __name__ == "__main__":
    slow_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    html_content = get_page(slow_url)
    print(html_content)
