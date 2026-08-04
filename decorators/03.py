#3. Create a decorator to convert function return value type
#Write a Python program to create a decorator to convert the return value of a function to a specified data type

def convert_to_data_type(data_type):
    def decorator(func):
        def wrapper(*args,**kwargs):

            result = func(*args,**kwargs)

            return data_type(result)
        return wrapper
    return decorator

@convert_to_data_type(str)
def function_that_return_number(num):
    return num


result = function_that_return_number(5)
print(result)
print(type(result))