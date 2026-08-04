#6. Implement a Decorator to Retry a Function on Failure

#Write a Python program that implements a decorator to retry a function multiple times in case of failure.
import time
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def retry(retries, delay):
    def decorator(func):

        def wrapper(*args, **kwargs):

            for i in range(retries):
                try:
                    if i > 0:
                        time.sleep(delay)
                    return func(*args, **kwargs)

                except Exception as e:
                    log.error(f"Retry: {i + 1} of Function {func.__name__} failed: {e}")
            raise Exception("Maximum retries exceeded. Function Failed")
        return wrapper
    
    return decorator

@retry(5,1)
def failing_func():
    raise TypeError("ERROR!!!")


failing_func()