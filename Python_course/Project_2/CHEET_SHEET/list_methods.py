#Lists - списки
'''
mylist = ["apple", "banana", "cherry"]

Метод	Описание на русском
append()	Добавляет элемент в конец списка.
clear()	Удаляет все элементы из списка (очищает список).
copy()	Возвращает копию списка.
count()	Считает, сколько раз указанный элемент встречается в списке.
extend()	Добавляет элементы из другого списка (или любого итерируемого объекта) в конец текущего списка.
index()	Возвращает индекс первого вхождения указанного элемента.
insert()	Вставляет элемент в список по указанной позиции.
pop()	Удаляет и возвращает элемент из списка по указанному индексу (по умолчанию последний элемент).
remove()	Удаляет первое вхождение элемента с указанным значением.
reverse()	Меняет порядок элементов в списке на обратный.
sort()	Сортирует элементы списка (по умолчанию — по возрастанию).
'''
#попробовать каждый метод

test_list1 = ["apple", "banana", "cherry"]
print(test_list1.append("orange"))  # None (метод изменяет список на месте)
print(test_list1)  # ['apple', 'banana', 'cherry', 'orange']

print(test_list1.clear())  # None (список очищен)
print(test_list1)  # []

test_list2 = ["apple", "banana", "cherry"]
test_list3 = test_list2.copy()
print(test_list3)  # ['apple', 'banana', 'cherry']

print(test_list2.count("banana"))  # 1
print(test_list2.count("orange"))  # 0

print(test_list2.index("banana"))  # 1
#print(test_list2.index("orange"))  # ValueError

print(test_list2.insert(1, "orange"))  # None (метод изменяет список на месте)
print(test_list2)  # ['apple', 'orange', 'banana', 'cherry']

print(test_list2.pop(1))  # orange
print(test_list2)  # ['apple', 'banana', 'cherry']

print(test_list2.remove("banana"))  # None (метод изменяет список на месте)
print(test_list2)  # ['apple', 'cherry']

print(test_list2.reverse())  # None (метод изменяет список на месте)
print(test_list2)  # ['cherry', 'apple']


print(test_list3.sort())  # None (метод изменяет список на месте)
print(test_list3)  # ['apple', 'banana', 'cherry']
print(test_list3.sort(reverse=True))  # None (метод изменяет список на месте)
print(test_list3)  # ['cherry', 'banana', 'apple']

# A function that returns the length of the value:
def my_func(e):
  return len(e)

cars = ['Ford', 'Mitsubishi', 'BMW', 'VW']

cars.sort(reverse=True, key=my_func)
print(cars)  # ['Mitsubishi', 'BMW', 'Ford', 'VW']

# Функция, возвращающая значение 'year':
def get_year(e):
  return e['year']

cars = [
  {'car': 'Ford', 'year': 2005},
  {'car': 'Mitsubishi', 'year': 2000},
  {'car': 'BMW', 'year': 2019},
  {'car': 'VW', 'year': 2011}
]

cars.sort(key=get_year)
print(cars)  
''' 
[{'car': 'Mitsubishi', 'year': 2000}, 
{'car': 'Ford', 'year': 2005}, 
{'car': 'VW', 'year': 2011}, 
{'car': 'BMW', 'year': 2019}]
'''

