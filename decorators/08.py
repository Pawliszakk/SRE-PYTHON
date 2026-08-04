#8. Implement a Decorator to Add Logging Functionality

#Write a Python program that implements a decorator to add logging functionality to a function.

import logging 
import time

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)



def log_function(func):
    def wrapper(*args,**kwargs):

        log.info(f"Starting {func.__name__} function...")

        result = func(*args, **kwargs)
        log.info(f"Function {func.__name__} ended")

        return result

    return wrapper


@log_function
def my_func():
    time.sleep(2)
    log.info("Success!")

my_func()