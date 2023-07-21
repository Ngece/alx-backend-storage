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
        """ Method that stores input data in Redis using a
            random key and returns the key """
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float]:
        """ Method that gets the value of a string key """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """ Method that converts bytes to string """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """ Method that converts bytes to int """
        return self.get(key, int)
    
    @replay
    def get_list(self, key: str) -> list:
        """ Method that converts bytes to list """
        return self.get(key, list)
    
    def get_kv(self, key: str) -> tuple:
        """ Method that converts bytes to tuple """
        return self.get(key, tuple)
    
    def get_float(self, key: str) -> float:
        """ Method that converts bytes to float """
        return self.get(key, float)
    
    def append(self, key: str, value: str) -> None:
        """ Method that appends a value to the key """
        self._redis.append(key, value)

    def get_str(self, key: str) -> str:
        """ Method that converts bytes to string """
        return self.get(key, str)
    
    def get_int(self, key: str) -> int:
        """ Method that converts bytes to int """
        return self.get(key, int)
    
    def get_list(self, key: str) -> list:
        """ Method that converts bytes to list """
        return self.get(key, list)
    
    def get_kv(self, key: str) -> tuple:
        """ Method that converts bytes to tuple """
        return self.get(key, tuple)
    
    def get_float(self, key: str) -> float:
        """ Method that converts bytes to float """
        return self.get(key, float)
    
    def append(self, key: str, value: str) -> None:
        """ Method that appends a value to the key """
        self._redis.append(key, value)

if __name__ == "__main__":
    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    cache.store(3.14159)
    cache.store([1, 2, 3])
    cache.store({"n": 42, "f": 3.14159, "foo": "bar"})
    print(cache.get_str("foo"))
    print(cache.get_str("does_not_exist"))
    print(cache.get_int("foo"))
    print(cache.get_int("does_not_exist"))
    print(cache.get_list("foo"))
    print(cache.get_list("does_not_exist"))
    print(cache.get_kv("foo"))
    print(cache.get_kv("does_not_exist"))
    print(cache.get_float("foo"))
    print(cache.get_float("does_not_exist"))
    cache.append("foo", "bar")
    print(cache.get_str("foo"))

    print("--")
    cache.store(42)
    cache.store(42)
    cache.store(42)
    cache.store(42)
    cache.store(42)
    cache.store(42)
    cache.store(42)
    cache.store(42)
    cache.store(42)
    print(cache.get_int("42"))
    print(cache.get_int("42"))
    print(cache.get_int("42"))
    print(cache.get_int("42"))
    print(cache.get_int("42"))
    print(cache.get_int("42"))
    print(cache.get_int("42"))
    print(cache.get_int("42"))
    print(cache.get_int("42"))
    print(cache.get_int("42"))

    print("--")
    cache.store("foo")
    cache.store("foo")
    cache.store("foo")
    cache.store("foo")
    cache.store("foo")
    cache.store("foo")
    cache.store("foo")
    cache.store("foo")
    cache.store("foo")
    print(cache.get_str("foo"))
    print(cache.get_str("foo"))
    print(cache.get_str("foo"))
    print(cache.get_str("foo"))
    print(cache.get_str("foo"))
    print(cache.get_str("foo"))
    print(cache.get_str("foo"))
    print(cache.get_str("foo"))
    print(cache.get_str("foo"))

    print("--")
    cache.store([1, 2, 3])
    cache.store([1, 2, 3])
    cache.store([1, 2, 3])
    cache.store([1, 2, 3])
    cache.store([1, 2, 3])
    cache.store([1, 2, 3])
    cache.store([1, 2, 3])
    print(cache.get_list("foo"))
    print(cache.get_list("foo"))
    print(cache.get_list("foo"))
    print(cache.get_list("foo"))
    print(cache.get_list("foo"))
    print(cache.get_list("foo"))
    print(cache.get_list("foo"))

    print("--")
    cache.store({"n": 42, "f": 3.14159, "foo": "bar"})
    cache.store({"n": 42, "f": 3.14159, "foo": "bar"})
    cache.store({"n": 42, "f": 3.14159, "foo": "bar"})
    cache.store({"n": 42, "f": 3.14159, "foo": "bar"})
    cache.store({"n": 42, "f": 3.14159, "foo": "bar"})
    print(cache.get_kv("foo"))
    print(cache.get_kv("foo"))
    print(cache.get_kv("foo"))
    print(cache.get_kv("foo"))
    print(cache.get_kv("foo"))