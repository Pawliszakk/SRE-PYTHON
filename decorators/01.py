# https://www.w3resource.com/python-exercises/decorator/
# 1. Create a Decorator to Log Function Arguments and Return Value
# Write a Python program to create a decorator that logs the arguments and return value of a function.

import logging

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


def decorator_one(func):

    def wrapper(*args,**kwargs):

        log.info(f"args={args} kwargs={kwargs}")
        
        result = func(*args, **kwargs)

        log.info(f"return={result}")

        return result

    return wrapper


@decorator_one
def my_func(first, second):
    return

my_func("one","two")