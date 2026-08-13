print("Hello, World!")

rrr = 2
print(id(rrr))

f = 10
if f > 5: print("f is greater than 5")
else: print("f is not greater than 5")

person = {"name": "Anna", "age": 25}

def greeting(name, age):
    print(f"Привет, {name}! Тебе {age} лет.")

greeting(**person)