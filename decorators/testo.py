

import logging
import time

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


def retry(retries, delay):
    def decorator(func):
        def wrapper(*args,**kwargs):
            for i in range(retries):
                try:
                        if i > 0:
                            time.sleep(delay)

                        log.info(f"Trying to run {func.__name__} for {i} time...")

                        result = func(*args,**kwargs)

                        return result

                except Exception as e:

                    log.error(f"Error occured: {e}")

        return wrapper
    return decorator

@retry(5,1)
def always_fail():
    raise TypeError("Something went wrong...")

always_fail()