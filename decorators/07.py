#7. Implement a Decorator to Enforce Rate Limits on a Function

#Write a Python program that implements a decorator to enforce rate limits on a function.
import logging
import time

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)




def rate_limit(max_calls, period):
    def decorator(func):
        calls = 0
        last_reset = time.time()
        def wrapper(*args,**kwargs):
            nonlocal calls, last_reset

            elapsed = time.time() - last_reset

            if elapsed > period:
                calls = 0
                last_reset = time.time()

            if calls >= max_calls:
                raise Exception("Rate limit exceeded. Please try again later")
            time.sleep(1)
            calls += 1
            return func(*args,**kwargs)
        return wrapper
    return decorator



@rate_limit(6,10)
def call_api():
    log.info("Calling api 10.42.40.1...")

for i in range(8):
    try:
        call_api()
    except Exception as e:
        log.error(e)