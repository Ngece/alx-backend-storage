#!/usr/bin/env python3
""" Module for using redis in Python """

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Count the number of times a method is called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ Wrapper function """
        self._redis.incr(key)
        return method(self, *args, **kwds)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ Store the history of inputs and outputs for a particular function """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ Wrapper function """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)

        output = str(method(self, *args, **kwds))
        self._redis.rpush(method.__qualname__ + ":outputs", output)

        return output

    return wrapper


def replay(method: Callable):
    """ Display the history of calls of a particular function """
    r = redis.Redis()
    name = method.__qualname__
    count = r.get(name).decode('utf-8')
    inputs = r.lrange(name + ":inputs", 0, -1)
    outputs = r.lrange(name + ":outputs", 0, -1)

    print("{} was called {} times:".format(name, count))
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))
    return method


class Cache:
    """ Cache class """
    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generate a random key, store the input data in Redis using the
            random key and return the key
        """
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str,
                                                                     bytes,
                                                                     int,
                                                                     float]:
        """ Convert data back to desired format """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Convert data to string """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """ Convert data to int """
        return self.get(key, int)
    
    def get_str_list(self, key: str) -> list:
        """ Convert data to list """
        return self.get(key, list)
    
    def get_int_list(self, key: str) -> list:
        """ Convert data to list """
        return self.get(key, lambda d: [int(e) for e in d])
    
    @replay
    def fibonacci(self, n: int) -> int:
        """ Compute the nth value of the Fibonacci sequence """
        if n <= 1:
            return n
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)
    
    def replay(self):
        """ Display the history of calls of a particular function """
        r = redis.Redis()
        name = self.fibonacci.__qualname__
        count = r.get(name).decode('utf-8')
        inputs = r.lrange(name + ":inputs", 0, -1)
        outputs = r.lrange(name + ":outputs", 0, -1)

        print("{} was called {} times:".format(name, count))
        for i, o in zip(inputs, outputs):
            print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                         o.decode('utf-8')))
            
if __name__ == "__main__":
    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    cache.store([1, 2, 3])
    cache.store({"n": 42, "foo": "bar"})
    print(cache.get_str("foo"))
    print(cache.get_str("does_not_exist"))
    print(cache.get_int("foo"))
    print(cache.get_int("does_not_exist"))
    print(cache.get_str_list("foo"))
    print(cache.get_str_list("does_not_exist"))
    print(cache.get_int_list("foo"))
    print(cache.get_int_list("does_not_exist"))
    print(cache.store(5))
    print(cache.store(6))
    print(cache.store(7))
    print(cache.store(8))
    print(cache.store(9))
    cache.reply()
    