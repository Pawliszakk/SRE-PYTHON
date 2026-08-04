#9. Implement a decorator to handle exceptions with a default value

#Write a Python program that implements a decorator to handle exceptions raised by a function and provide a default response

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def default_exception(default_value):
    def decorator(func):
        def wrapper(*args,**kwargs):
            try:
                result = func(*args,**kwargs)
                return result
            except Exception as e:
                log.error(f"Default exception! {e}")
                return default_value
        return wrapper

    return decorator

@default_exception("Yooo value")
def always_fail():
    raise TypeError("Sth went wrong")

always_fail()