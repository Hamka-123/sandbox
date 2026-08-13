""" 1️⃣ Immutable объекты (int, str, tuple, frozenset)
Код	Объект a	Объект b	a is b	Пояснение
a = 10
b = 10	10	10	True	Python кэширует маленькие целые числа (-5..256)
a = 1000
b = 1000	1000	1000	False	Большие числа создают отдельные объекты
a = "hello"
b = "hello"	"hello"	"hello"	True	Строки могут интернироваться
a = (1, 2)
b = (1, 2)	(1,2)	(1,2)	False	Каждая кортежная литерал создаёт новый объект
2️⃣ Mutable объекты (list, dict, set, bytearray)
Код	Объект a	Объект b	a is b	Пояснение
a = [1,2,3]
b = a	[1,2,3]	[1,2,3]	True	b ссылается на тот же список, что и a
a = [1,2,3]
b = a.copy()	[1,2,3]	[1,2,3]	False	copy() создаёт новый объект
a = {"x":1}
b = {"x":1}	{"x":1}	{"x":1}	False	Отдельные словари, разные объекты
a = set([1,2])
b = a	{1,2}	{1,2}	True	Ссылки на один и тот же объект
3️⃣ Изменение mutable объекта
a = [1,2,3]
b = a       # True, a is b
b.append(4) # Изменяем b
print(a)    # [1,2,3,4] – a тоже изменился


✅ Важно: mutable объекты изменяются по ссылке, все переменные, указывающие на объект, видят эти изменения.

4️⃣ Изменение immutable объекта
a = 10
b = a       # True, a is b
b += 5      # Создаётся новый объект 15 для b
print(a)    # 10 – a не изменился
print(b)    # 15
print(a is b) # False


✅ Immutable объекты не изменяются, любые операции создают новый объект. """


'''
What prints?

def outer():
    x=10
    def inner(): return x
    return inner

print(outer()())
Python advanced. Function.
10
Error
None
x


def f(a, **kwargs):
    return kwargs.get('b', 0) + a

print(f(5, b=10))


Can dictionary keys be of any type?
Python advanced. List. Tuple. Dictionary. Set.
Yes
Only strings
Only numbers
Only immutable types

What is the correct way to read a file line by line?

Python basics. Files. CSV. JSON.
file = open("example.txt", "r") for line in file: print(line) file.close()
file = open("example.txt", "r") print(file.readlines()) file.close()
file = open("example.txt", "r") content = file.read() print(content) file.close()
All of the above

/ 
//

'''
def f(x, items=[1,2,3]):
    items.append(x)
    return items

print(f(1))
print(f(2))