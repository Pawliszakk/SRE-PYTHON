def add_salami(func):
    def wrapper(*args,**kwargs):
        print("Dodalismy salami! 🫥")
        func(*args,**kwargs)
    return wrapper

def add_pepperona(func):
    def wrapper(*args,**kwargs):
        print("Dodalismy pepperone!!!")
        func(*args,**kwargs)
    return wrapper

@add_salami
@add_pepperona
def create_pizza(pizza_name,pizza_size):
    print(f"Here is your {pizza_size}cm {pizza_name} pizza!")

create_pizza("Capricossa","42")