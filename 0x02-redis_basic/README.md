exercise.py:
Creates a Cache class. In the __init__ method, stores an instance of the Redis client as a private variable named _redis (using redis.Redis()) and flushes the instance using flushdb.

Creates a store method that takes a data argument and returns a string. The method generates a random key (e.g. using uuid), store the input data in Redis using the random key and return the key.

Implements a system to count how many times methods of the Cache class are called.

Above Cache defines a count_calls decorator that takes a single method Callable argument and returns a Callable.

As a key, uses the qualified name of method using the __qualname__ dunder method.

Creates and returns a function that increments the count for that key every time the method is called and returns the value returned by the original method.

Defines a call_history decorator to store the history of inputs and outputs for a particular function.

Everytime the original function will be called, adds its input parameters to one list in redis, and stores its output into another list.

In call_history, uses the decorated function’s qualified name and appends ":inputs" and ":outputs" to create input and output list keys, respectively.

call_history has a single parameter named method that is a Callable and returns a Callable.

In the new function that the decorator will return, uses rpush to append the input arguments.

Implements a replay function to display the history of calls of a particular function.





web.py:
Implements a get_page function (prototype: def get_page(url: str) -> str:). It uses the requests module to obtain the HTML content of a particular URL and returns it.

Inside get_page it tracks how many times a particular URL was accessed in the key "count:{url}" and caches the result with an expiration time of 10 seconds.