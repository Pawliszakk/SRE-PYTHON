#2. Create a Decorator to Measure Function Execution Time
#Write a Python program to create a decorator function to measure the execution time of a function.
import logging
import time

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)



def execution_counter(func):
    def wrapper(*args,**kwargs):

        start = time.perf_counter()

        func(*args,**kwargs)

        end = time.perf_counter()

        time_result = end - start

        log.info(f"Function: {func.__name__} executed in: {time_result} seconds")
    return wrapper



@execution_counter
def sleepy_function(sleep_seconds):
    time.sleep(sleep_seconds)


sleepy_function(1)