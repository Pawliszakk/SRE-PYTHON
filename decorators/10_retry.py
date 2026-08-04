import time

def retry(func):
    def wrapper(*args,**kwargs):

        for i in range(3):
            try:
                if i > 0:
                    time.sleep(1)

                return func(*args,**kwargs)
            
            except Exception as e:

                print(f"Retry {i + 1 } failed: {e}")

        print("All retries failed.")
        
    return wrapper

@retry
def always_fail():
    raise ValueError("Sth went wrong")

always_fail()