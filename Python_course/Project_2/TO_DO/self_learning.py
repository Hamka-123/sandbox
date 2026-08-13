#✅TODO: 1️⃣ Основы Python
'''
✅ Переменные и типы данных: int, float, str, преобразование типов
✅ Ввод/вывод данных: input(), print(), f-строки
✅ Базовые операции: арифметические, сравнение, логические
✅ Условные конструкции: if-else
✅ Работа со строками: базовые операции, форматирование
✅ Коллекции: списки, кортежи, словари, множества - создание, методы, операции
✅ Работа с функциями: range(), type(), методы коллекций
'''
##✅TODO: - Запросить имя и возраст пользователя, вывести приветствие
'''
name = input("Введите имя:")
age = int(input("Введите возраст:"))
print(f'Привет {name} ({age})')
'''
##✅TODO: - Преобразовать строку в int и float и посчитать их сумму
string_1 = '876'
int_1 = int(string_1)
float_1 = float(string_1)
print(int_1 + float_1)
##✅TODO: - Проверить, является ли число чётным или нечётным
'''
number = int(input("Введите число: "))
if number % 2 == 0: print (f'Число {number} четное')
else: print (f'Число {number} НЕ четное')
'''
##✅TODO: - Считать площадь и периметр прямоугольника по введённым сторонам
""" width = int(input("Ширина (см):"))
height = int(input("Высота (см):"))
print('Площадь прямоугольника:',width*height,'см','Периметр прямоугольника:',(width+height)*2)
 """
##✅TODO: - Использовать f-строки для форматированного вывода
print(f'Я использую f-строку для вывода переменной string_1 и её значение = {string_1} ')

#✅TODO: 2️⃣ Списки и кортежи
##✅TODO: - Создать список чисел, добавить элемент, удалить элемент, вывести срез
list1 = list(range(10))
print(type(list1))
list1.append(10)
list1.remove(0)
print(list1)
print(list1[0:5])
##✅TODO: - Отсортировать список по убыванию, затем развернуть
list1.sort(reverse=True)
print(list1)
list1 = list1[::-1]
print(list1)
##✅TODO: - Создать tuple и найти индекс элемента, посчитать количество вхождений
tuple_1 = tuple((1,3,7,54,3,5,8,5,9,4))
print(type(tuple_1))
i = tuple_1.index(5)
count = tuple_1.count(5)
print(tuple_1[i],' встречается раз: ',count)

#✅TODO: 3️⃣ Словари и множества
##✅TODO: - Создать словарь студентов и оценок, обновить словарь
dict_1 = {
    "Anna": 5,
    "Irina": 3,
    "Vika": 4,
    "Igor": 2
} 
print(type(dict_1))
dict_1.update({"Maya": 5})
print(dict_1)

##✅TODO: - Создать словарь и использовать get, setdefault, pop, popitem
dict_3 = dict(dict_1)
dict_3.pop("Anna")
dict_4 = dict_3.copy()
dict_3.setdefault("Anna", 4)
dict_3.popitem()
dict_4.clear()
dict_3 = dict.fromkeys(dict_1,0)
print(dict_4.get("Irina"))
print(dict_3)
print(dict_4)
##✅TODO: - Создать два множества, выполнить union, intersection, difference
set1 = {"1","2","3"}
set2 = set("3")
set3 = set1.union(set2)
set4 = set1.intersection(set2)
set5 = set1.difference(set2)
print(type(set3))
print(set3)
print(set4)
print(set5)
##✅TODO: - Использовать set для удаления дубликатов в списке
list2 = [1,3,5,6,4,3,2,4,41,1,124]
set6 = set(list2)
print(set6)

#✅TODO: 🔹 Задачи на словари:
##✅TODO: 1. Объединение двух словарей (при конфликте брать значения из второго)
dict1 = {'a': 1, 'b': 2, 'c': 3}
dict2 = {'b': 20, 'd': 4}
dict3 = dict1 | dict2 #v1
dict1.update(dict2) #v2 обновление первого
dict4 = {**dict1, **dict2} #v3 распаковка
dict5 = dict1.copy() #v4
for k,v in dict2.items():
    dict5[k] = v
    
dict5 = {k: dict1.get(k,0) + dict2.get(k,0) for k in dict1.keys() | dict2.keys()} #v5 операции с элементами
print(dict3)
print(dict4)
print(dict5)

##✅TODO: 2. Найти ключ с максимальным значением
grades = {'Anna': 5, 'Ivan': 3, 'Maria': 4, 'Petr': 5}
#v1
max_key = max(grades, key=grades.get)
print(max_key)
#v2
max_key = None
max_value = 0
for k, v in grades.items():
    if v > max_value:
        max_key = k
        max_value = v

print(max_key, max_value)

##✅TODO: 3. Инвертировать словарь (поменять ключи и значения местами)
original_dict = {'a': 1, 'b': 2, 'c': 3}
new_dict = {}
for k,v in original_dict.items():
    new_dict.update({v:k})
print(new_dict)
# 4. Подсчитать частоту слов в списке
words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
#words_dict = {w: words.count(w) for w in set(words)}
'''
words_dict = {k:0 for k in words}
for i in words:
    words_dict[i] += 1
'''
words_dict = {}
for w in words:
    words_dict[w] = words_dict.get(w, 0) + 1

print(words_dict)

##✅TODO: 5. Получить значение из вложенного словаря
students = {
    'Anna': {'math': 5, 'physics': 4},
    'Ivan': {'math': 3, 'physics': 5}
}
print(students['Anna']['math'])

##✅TODO: 6. Отфильтровать словарь, оставив только оценки ≥ 4
grades = {'Anna': 5, 'Ivan': 3, 'Maria': 4, 'Petr': 2}
new_grades = {k: v for k,v in grades.items() if v >= 4}
print(new_grades)

##✅TODO:7. Создать словарь из двух списков
keys = ['name', 'age', 'city']
values = ['Anna', 25, 'Moscow']
#v1
dict_5 = dict(zip(keys, values))
print(dict_5)
#v2
dict6 = {keys[i]:values[i] for i in range(len(keys)) }
print(dict6)
#v3
dict7 = dict.fromkeys(keys, None)
# Обновляем значения
for i in range(len(keys)):
    dict7[keys[i]] = values[i]

print(dict7)

##✅TODO: 8. Удалить все элементы с значениями None
data = {'a': 1, 'b': None, 'c': 3, 'd': None}
data = {k:v for k,v in data.items() if v is not None}
print(data)

#✅TODO: 🔹 Задачи на множества:
##✅TODO: 1. Удалить все четные числа из множества
numbers = {1, 2, 3, 4, 5, 6}
numbers_without_even = set(i for i in numbers if i%2 != 0)
print(numbers_without_even)

##✅TODO: 2. Найти общие элементы в трех множествах
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
set3 = {4, 5, 6, 7}

set4 = set1 & set2 & set3
print(set4)

##✅TODO: 3. Проверить, является ли множество подмножеством другого
set_a = {1, 2}
set_b = {1, 2, 3, 4, 5}
print(set_a <= set_b)

##✅TODO: 4. Найти элементы, которые есть только в одном из множеств
set_x = {1, 2, 3, 4}
set_y = {3, 4, 5, 6}

print((set_x - set_y) | (set_y - set_x)) # difference() + union()
print(set_x ^ set_y) # symmetric_difference

##✅TODO: 5. Создать множество из строки (уникальные символы)
text = "hello world"
print(set(text))

##✅TODO: 6. Удалить дубликаты из списка и сохранить порядок
numbers_list = [3, 1, 2, 3, 4, 2, 1, 5]
unique_numbers = list(dict.fromkeys(numbers_list))
print(set(numbers_list))
print(unique_numbers)

##✅TODO: 7. Найти симметрическую разность трех множеств
set1 = {1, 2, 3}
set2 = {2, 3, 4}
set3 = {3, 4, 5}

print(set1 ^ set2 ^ set3)

##✅TODO: 8. Проверить, есть ли общие элементы у двух множеств
set_a = {1, 2, 3}
set_b = {4, 5, 6}
print(set_a.isdisjoint(set_b))
common = set_a.intersection(set_b)  # то же самое, что set_a & set_b
if common:
    print("Есть общие элементы:", common)
else:
    print("Общих элементов нет")


#✅TODO:🔹 Комбинированные задачи:
##✅TODO: 1. Найти общие ключи в двух словарях
dict1 = {'a': 1, 'b': 2, 'c': 3}
dict2 = {'b': 20, 'c': 30, 'd': 40}

print(dict1.keys() & dict2.keys())

##✅TODO: 2. Преобразовать список словарей в словарь списков
data = [
    {'name': 'Anna', 'age': 25},
    {'name': 'Ivan', 'age': 30},
    {'name': 'Maria', 'age': 28}
]
data_trans = {k: [d[k] for d in data] for k in data[0]}
print(data_trans)


##✅TODO:3. Найти самые частые слова в тексте
text = "apple banana apple orange banana apple"
words = text.split()
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1
print(freq)

most_common_word = max(freq, key=freq.get)
print(most_common_word, freq[most_common_word])

##✅TODO: 4. Сгруппировать слова по первой букве
words = ['apple', 'banana', 'orange', 'apricot', 'berry']

group_dict = {}
for word in words:
    key = word[0]
    if key not in group_dict:
        group_dict[key] = []
    group_dict[key].append(word)
    
print(group_dict)

#✅TODO:🔹 Арифметика и математические функции:

# ------------------------------
# Арифметические операторы
# ------------------------------
# +   сложение
# -   вычитание
# *   умножение
# /   деление (результат float)
# //  целочисленное деление
# %   остаток от деления
# **  возведение в степень
# -a  унарный минус
# +a  унарный плюс

# ------------------------------
# Операторы присваивания с арифметикой
# ------------------------------
# +=  a += 5   → a = a + 5
# -=  a -= 5   → a = a - 5
# *=  a *= 5   → a = a * 5
# /=  a /= 5   → a = a / 5
# //= a //= 5  → a = a // 5
# %=  a %= 5   → a = a % 5
# **= a **= 5  → a = a ** 5

# ------------------------------
# Сравнение
# ------------------------------
# ==  равно
# !=  не равно
# >   больше
# <   меньше
# >=  больше или равно
# <=  меньше или равно

# ------------------------------
# Логические операторы
# ------------------------------
# and  логическое И
# or   логическое ИЛИ
# not  логическое НЕ

# ------------------------------
# Битовые операторы
# ------------------------------
# &   побитовое И
# |   побитовое ИЛИ
# ^   побитовое XOR
# ~   побитовое НЕ
# <<  сдвиг влево
# >>  сдвиг вправо

# ------------------------------
# Специальные операторы
# ------------------------------
# is        проверка на идентичность (тот же объект)
# is not    проверка на различие объектов
# in        проверка на вхождение в коллекцию
# not in    проверка на отсутствие в коллекции

# ------------------------------
# Полезные встроенные функции
# ------------------------------
# abs(a)       модуль числа
# round(a, n)  округление до n знаков
# divmod(a,b)  возвращает (частное, остаток)
# pow(a,b)     a в степени b
# min(a,b,...) минимальное значение
# max(a,b,...) максимальное значение
# sum(iterable) сумма элементов
# sorted(iterable) сортировка коллекции
# enumerate(iterable, start=0)  нумерация элементов
# zip(*iterables) объединение коллекций по индексам

'''
🎯 Что проверяют эти задачи:
Работу с математическими функциями
Манипуляции со строками
Сложные логические условия
Работу с датой и временем
Решение практических задач
Умение комбинировать разные концепции
'''
##✅TODO: 1. Посчитать гипотенузу прямоугольного треугольника по двум катетам
a = 3
b = 4
c = (a**2 + b**2)**0.5
print(f"Гипотенуза: {c}") 

'''
Синтаксис: {переменная:формат}
Основные спецификаторы:
f - дробное число
d - целое число
% - проценты
e - научная нотация
, - разделитель тысяч
b, o, x - системы счисления

# Разные системы счисления
print(f"Двоичное: {integer:b}")  # Двоичное: 101010
print(f"Восьмеричное: {integer:o}")  # Восьмеричное: 52
print(f"Шестнадцатеричное: {integer:x}")  # Шестнадцатеричное: 2a
print(f"Шестнадцатеричное (верхний регистр): {integer:X}")  # 2A
'''
""" c = 40450934593
print(f'{c:.1f}')
print(f'{c:3}')
print(f'{c:<3}')
print(f'{c:^3}')
print(f'{c:04}')
print(f'{c:,}')
print(f'{c:,.1f}')
print(f'{c:.1%}')
print(f'{c:.2%}')
print(f'{c:^10.2e}')
print(f'{c:+.2e}')
print(f'{c:-.2f}')
print(f'{c:b}')
print(f'{c:o}')
print(f'{c:x}')
print(f'{c:X}') """

##✅TODO: 2. Округлить число π до 3 знаков после запятой
pi = 3.1415926535
print(f'{pi:.3f}')

##✅TODO: 3. Проверить, делится ли число на 3 и на 5 одновременно
number = 15
if number % 3 == 0 and number % 5 == 0:
    print(f'Число делиться как на 3 так и на 5')

##✅TODO: 4. Найти целую часть и остаток от деления
dividend = 17
divisor = 5

quotient = dividend //  divisor
remainder = dividend % divisor
result = divmod(dividend,divisor) 

print(quotient, remainder)
print(result)

##✅TODO: 5. Возвести число в степень и найти квадратный корень
base = 4
exponent = 3

result = base ** exponent
square_root = base ** 0.5

print(result) # 4 ** 3 = 64
print(square_root) # √4 = 2.0

#✅TODO:🔹 Работа со строками:
##✅TODO: 1. Разделить строку на слова и объединить обратно
sentence = "Hello world from Python"
words = sentence.split(" ")
sentence_2 = ""
for i in words: 
    sentence_2 += i +" "
print(sentence_2.strip())

##✅TODO: 2. Перевести строку в верхний и нижний регистр
text = "Python Programming"
upeer_text = text.upper()
lower_text = text.lower()
print(upeer_text, lower_text)

##✅TODO: 3. Заменить все пробелы в строке на дефисы
phrase = "This is a test string"
print(phrase.replace(" ", "-"))

##✅TODO: 4. Проверить, начинается и заканчивается ли строка на определенные символы
filename = "document.txt"
print(filename.startswith("d"))
print(filename.endswith("t"))

##✅TODO: 5. Извлечь подстроку между двумя позициями
text = "abcdefghijk"
start = 2
end = 7
print (text[start:end])
#✅TODO:🔹 Логические операции:
##✅TODO: 1. Проверить, находится ли число в диапазоне от 10 до 20
x = 15
if 10 < x < 20:
    print('в указанном диапазоне')

##✅TODO: 2. Проверить, является ли год высокосным
year = 2024
'''
он делится на 4,
но не делится на 100,
или делится на 400.
'''
if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
    print("год высокосный")
else:
    print("год обычный")

##✅TODO: 3. Определить тип треугольника по сторонам
a, b, c = 3, 4, 5
if a + b > c and  a + c > b and b + c > a:
    if a == b == c:
        print("Равносторонний треугольник")
    elif a == b or b == c or a == c:
        print("Равнобедренный треугольник")
    elif a**2 + b**2 == c**2 or a**2 + c**2 == b**2 or b**2 + c**2 == a**2:
        print("Прямоугольный треугольник")
    else:
        print("Разносторонний треугольник")


##✅TODO: 4. Проверить, является ли строка палиндромом (читается одинаково в обеих сторон)
word = "radar"
print(word[::-1] == word)

##✅TODO: 5. Определить четверть координатной плоскости для точки
x, y = 3, -2
if x > 0 and y > 0: print("1 четверть")
elif x < 0 and y > 0: print("2 четверть")
elif x < 0 and y < 0: print("3 четверть")
elif x > 0 and y < 0: print("4 четверть")


#✅TODO:🔹 Работа с датой и временем:
from datetime import datetime, timedelta
import random
import string
'''
Импортируем from datetime import datetime, timedelta.
Получаем текущее время через now = datetime.now().
Парсим строку в дату с помощью .strptime(строка, шаблон).
Форматируем дату в строку с помощью .strftime(шаблон).
Выполняем арифметику с датами, используя timedelta.
Для сложных проектов подключаем pytz для работы с часовыми поясами.
%Y — год 4 цифры (2024)
%y — год 2 цифры (24)
%m — месяц числом (01-12)
%d — день месяца (01-31)
%H — час (00-23)
%M — минута (00-59)
%S — секунда (00-59)
%A — название дня недели (Monday, Tuesday...)
%B — название месяца (January, February...)
'''
##✅TODO: 1. Вывести текущую дату и время
##✅TODO: 2. Прибавить 5 дней к текущей дате
##✅TODO: 3. Найти разницу между двумя датами
date1 = datetime(2024, 1, 15)
date2 = datetime(2024, 2, 1)

print(datetime.now()) #1
print(datetime.now() + timedelta(days=5)) #2
print(date2 - date1) #3

##✅TODO: 4. Преобразовать строку в дату
date_str = "2024-03-15"
print(datetime.strptime(date_str, "%Y-%m-%d"))

##✅TODO: 5. Определить день недели для заданной даты
date = datetime.now()
print (date.strftime("%A"))
print(date.isoweekday())

#✅TODO:🔹 Комплексные задачи:
##✅TODO: 1. Конвертер температур: Цельсий → Фаренгейт → Кельвин
celsius = 25
farengeit = (celsius * 9/5) + 32
kelvin = (farengeit - 32) * 5/9 + 273.15
print("C",celsius , "-> F",farengeit, "-> K",kelvin)
##✅TODO: 2. Калькулятор ИМТ (индекс массы тела)
weight = 68  # кг
height = 1.75  # м
IMT = weight / (height)**2
print(IMT)
##✅TODO: 3. Генератор случайного пароля заданной длины
length = 12
    # Все возможные символы для пароля
characters = string.ascii_letters + string.digits + "!@#$%^&*"
    #Генерация пароля
password = ''.join(random.choice(characters) for _ in range(length))

print(f"Сгенерированный пароль: {password}")
##✅TODO: 4. Подсчет суммы цифр числа
number = 12345
print(str(number))
summ = 0
for i in str(number):
    summ = summ + int(i) 

#summ = sum(int(i) for i in str(number))
print(summ)

##✅TODO: 5. Определение времени суток по часам
hour = 14
if 0 <= hour < 8: print("Ночь") 
elif 8 <= hour < 12: print ("Утро")
elif 12 <= hour < 16: print("День")
elif 16 <= hour < 24: print("Вечер")

#✅TODO:🔹 Практика с коллекциями:
##✅TODO: 1. Найти второй по величине элемент в списке sort and sorted
numbers = [5, 2, 8, 1, 9, 3]
numbers.sort(reverse=True)
max_second = numbers[1]
print(max_second)

##✅TODO: 2. Перевернуть строку без использования reversed()
text = "hello"
print(text[::-1])

##✅TODO: 3. Найти все уникальные элементы в списке списков
nested_list = [[1, 2], [2, 3], [1, 4]]
unique = set(x for sublist in nested_list for x in sublist)
print(unique)

##✅TODO: 4. Объединить два словаря, суммируя значения одинаковых ключей
dict1 = {'a': 1, 'b': 2, 'c': 3}
dict2 = {'b': 3, 'c': 4, 'd': 5}

dict3 = {key: dict1.get(key, 0) + dict2.get(key, 0) for key in set(dict1) | set(dict2)}
print(dict3)

##✅TODO: 5. Сгенерировать список квадратов чисел от 1 до n
n = 10
squeres = [x**2 for x in range(1, n+1)]
print(squeres)
print("-----------------------------------------\n")


#TODO: 4️⃣ Bytes / bytearray
##TODO: - Преобразовать строку в bytes и bytearray
##TODO: - Изменить байт в bytearray

#TODO: 5️⃣ Mutable vs Immutable
##TODO: - Изменить список внутри функции и проверить оригинал
##TODO: - Попробовать изменить строку внутри функции и проанализировать результат
##TODO: - Сравнить поведение mutable и immutable объектов при копировании

#TODO: 6️⃣ Копирование объектов
##TODO: - Создать вложенный список, сделать shallow и deep copy, изменить внутренний элемент
##TODO: - Проверить, как копирование работает с кортежами и frozenset

#TODO: 7️⃣ Циклы и итерации
##TODO: - Использовать for и while для итераций
##TODO: - Использовать enumerate, zip, reversed, sorted
##TODO: - Применять break и continue в циклах
##TODO: - Создать list, dict и set comprehension
##TODO: - Создать generator expression

#TODO: 8️⃣ Работа с CSV и JSON
print("-"*100)
print('''
get path
dunder prop, method
''')
import os
print('1',__file__.split(os.sep))
print('2',__file__.split(os.sep)[-1])
print('3',os.sep.join(__file__.split(os.sep)[:-1]))
abs_path = r"c:\temp" #prefix r -> raw string

##TODO: - Прочитать CSV-файл и преобразовать в список списков
##TODO: - Преобразовать CSV в список словарей
##TODO: - Создать словарь словарей по уникальному ключу
##TODO: - Использовать NamedTuple и dataclass для строк CSV
##TODO: - Сериализовать структуру данных в JSON и обратно
##TODO: - Прочитать CSV с разными типами данных и корректно преобразовать типы
##TODO: - Экспортировать список словарей в новый CSV

#TODO: 9️⃣ Встроенные функции и конструкторы
##TODO: - Использовать len, type, isinstance, id, sum, min, max
##TODO: - Использовать dict(), list(), set(), tuple(), frozenset()
##TODO: - Применять sorted(), map(), filter()
##TODO: - Использовать all(), any() для проверки условий
##TODO: - Использовать zip() с unpacking для транспонирования списка списков

#TODO: 🔟 Практические навыки
##TODO: - Группировать и фильтровать данные в списках и словарях
##TODO: - Пройти по nested structures и извлечь данные
##TODO: - Преобразовать данные между типами
##TODO: - Проверить независимость объектов после копирования
##TODO: - Прочитать CSV с продажами, сгруппировать по товару и вычислить среднюю цену
##TODO: - Создать nested dict для студентов и оценок, отфильтровать лучших
##TODO: - Использовать list comprehension и filter для выборки чисел
##TODO: - Прочитать текстовый файл, подсчитать уникальные слова и вывести 10 самых частых
'''
#✅TODO: 1️⃣1️⃣ Функции

##✅TODO: - Написать функцию с обязательными и необязательными аргументами
def func(x,y,key_arg = 5,**kwargs):
    print(x,y,key_arg, kwargs['a'])

func(1,2,3,a = 2)

##✅TODO: - Использовать *args и **kwargs для переменного числа аргументов
def func2(*args, **kwargs):
    print('args: ',args)
    print('kwargs: ', kwargs)
    
func2(3,5,7,2,6,7,a=1, b=2)
##✅TODO: - Написать рекурсивную функцию (например, факториал)
def factorial(num):
    if num <= 1:
        return 1
    else: return num * factorial(num - 1)
    
print(factorial(5))
##✅TODO: - Написать функцию, возвращающую несколько значений через tuple
def func2():
    c = 1
    t = 2
    s = 3
    return (c,t,s) # возвращаем кортеж (tuple)

print(func2())
'''
#TODO: лямбда функции
'''

# 📍 Лямбда с несколькими аргументами
area = lambda w, h: w * h
in_range = lambda x, min_val, max_val: min_val <= x <= max_val
average = lambda *args: sum(args) / len(args)

# 📍 Рекурсивные лямбды (требуют присваивания переменной)
factorial = lambda n: 1 if n <= 1 else n * factorial(n-1)
fibonacci = lambda n: n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)

# 📍 Обработка данных с лямбдами
transactions = [{"amount": 100, "type": "income"}, {"amount": 50, "type": "expense"}]
total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
food_expenses = sum(t['amount'] for t in transactions if t.get('category') == 'food')
'''
'''
##✅TODO: 📍 Базовые лямбда-функции
# Создайте лямбда-функции для: удвоения числа, проверки четности, преобразования в верхний регистр, объединения строк
double = lambda x: x*2
is_even = lambda x: x%2 == 0
upper_case = lambda x: x.upper()
concat = lambda a,b: f'{a} {b}'

##✅TODO: 📍 Фильтрация списков с filter()
# Отфильтруйте: четные числа, числа больше 5, слова длиннее 5 символов, слова на букву 'a'
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda n: n % 2 == 0, numbers))
greater_than_five = list(filter(lambda e: e > 5, numbers))
words = ['sfasf', 'safasf', 'sdfsdf','asdasf', 'aaa']
words_great_6 = list(filter(lambda w: len(w) > 5, words ))
words_start_a = list(filter(lambda w: w.startswith('a'), words))

##✅TODO: 📍 Сортировка сложных структур с sorted()
# Отсортируйте список словарей: по возрасту, по оценке (убывание), по длине имени, по кастомному условию
students = [{"name": "Alice", "age": 20, "grade": 2}, {"name": "Bob", "age": 22, "grade": 5}]
by_age = sorted(students, key=lambda s: s['age'])
by_grade_desc = sorted(students, key=lambda s: s['grade'], reverse=True)
by_name_len = sorted(students, key=lambda s: len(s['name']))
by_custom = sorted(students, key=lambda s: (s['grade'] < 5, s['age'] < 21))

print(by_custom)

##✅TODO: 📍 Преобразования с map()
#Преобразуйте данные: в формат "Имя: возраст", рассчитайте год рождения, добавьте флаг совершеннолетия
data = [("John", 17), ("Jane", 30)]
formatted = list(map(lambda x: f"{x[0]}: {x[1]}", data))
birth_years = list(map(lambda x: 2025 - x[1], data))
adult_flag = list(map(lambda x: (x[0], x[1], "adult" if x[1] >= 18 else "minor") , data))
print(adult_flag)
'''
##TODO: 📍 Лямбда с несколькими аргументами
# Создайте лямбды: расчет площади, проверка диапазона, форматирование имени, среднее арифметическое


##TODO: 📍 Рекурсивные лямбды
# Реализуйте через лямбду: факториал, числа Фибоначчи (требуют присваивания переменной)

##TODO: 📍 Обработка данных с лямбдами
# Обработайте транзакции: сумма доходов, расходы по категориям, сортировка, группировка

##TODO: 📍 Лямбда в функциях высшего порядка
# Создайте функцию, которая принимает лямбды-условия и применяет их к данным

##TODO: 📍 Комбинация лямбд с *args и **kwargs
# Напишите лямбды, которые работают с переменным числом аргументов
'''
Напиши функцию summarize(title, *scores, **info), которая:
Выводит название (title)
Считает среднее значение scores
Выводит все данные из info

#TODO:1️⃣ Объединение словарей

Напиши функцию merge_dicts(*dicts, **extra)

Принимает любое количество словарей через *dicts

Принимает дополнительные ключи через **extra

Возвращает один словарь, где при конфликте ключей приоритет у последнего словаря или у extra

#TODO:2️⃣ Фильтр чисел по диапазону

Напиши функцию filter_range(min_val, max_val, *numbers)

Принимает минимум и максимум

Любое количество чисел через *numbers

Возвращает список чисел, попадающих в диапазон [min_val, max_val]

#TODO:3️⃣ Создание HTML-элемента

Напиши функцию html_tag(tag, content, **attrs)

Принимает название тега tag и содержимое content

Любое количество атрибутов через **attrs

Возвращает строку с HTML-элементом

#TODO:4️⃣ Сумма факториалов

Напиши функцию factorial_sum(*numbers)

Принимает любое количество чисел через *numbers

Возвращает сумму факториалов этих чисел

Используй рекурсивную функцию для вычисления факториала

#TODO:5️⃣ Сортировка словаря по значениям

Напиши функцию sort_dict(**kwargs)

Принимает произвольное количество ключ-значение через **kwargs

Возвращает словарь, отсортированный по значениям по возрастанию

#TODO:6️⃣ Объединение списков

Напиши функцию combine_lists(*lists, **options)

Принимает любое количество списков через *lists

Через **options может принимать опцию unique=True/False для удаления дубликатов

Возвращает один объединённый список
'''
'''
#TODO: 1️⃣2️⃣ Обработка исключений
##✅TODO: - Обработать деление на ноль
try: 
    x = a/0
except ZeroDivisionError as e:
    print(e)
##✅TODO: - Прочитать файл и обработать FileNotFoundError
try:
    f = open("file.txt", "r")
except FileNotFoundError as e:
    print(e)
##✅TODO: - Использовать try/except/else/finally для обработки ошибок
try:
    if 0 != 0:
        raise Exception("Error")
except Exception as e:
    print(e)
else: print("ok")
finally: print("Done")
'''

#TODO: 1️⃣3️⃣ Работа с файлами
##TODO: - Прочитать текстовый файл и подсчитать количество строк, слов и символов
##TODO: - Записать список чисел в файл и прочитать его обратно
##TODO: - Использовать менеджер контекста with для работы с файлами

#TODO: 1️⃣4️⃣ Регулярные выражения
##TODO: - Найти все email-адреса в тексте
##TODO: - Проверить, является ли строка корректным телефоном
##TODO: - Заменить все числа в тексте на символ "#"

#TODO: 1️⃣5️⃣ Модули и пакеты
##TODO: - Импортировать модуль math и использовать sqrt, ceil, floor
##TODO: - Создать свой модуль с функцией и импортировать его в другом файле
##TODO: - Использовать random для генерации случайного числа и выбора случайного элемента

#TODO: 1️⃣6️⃣ ООП
##TODO: - Создать класс "Книга" с атрибутами title, author, year
##TODO: - Добавить метод, возвращающий описание книги
##TODO: - Создать наследника класса "ЭлектроннаяКнига" с дополнительным атрибутом size_mb
##TODO: - Использовать property для получения и установки значения с проверкой

#TODO: 1️⃣7️⃣ Декораторы и функции высшего порядка
##TODO: - Написать декоратор, измеряющий время выполнения функции
##TODO: - Создать функцию, принимающую другую функцию и список, применяя функцию к каждому элементу
