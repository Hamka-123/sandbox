'''
| Парадигма                          | Основная идея                                                                                       | Требования / принципы                                                                                                                                                               | Python поддержка                                  | Примеры языков                       | Примеры на Python                                                                                                                                                                           |
| ---------------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Процедурное**                    | Программа состоит из последовательностей процедур (функций), которые выполняют действия над данными | - Чёткая структура функций<br>- Параметры и локальные переменные<br>- Минимизация глобальных переменных<br>- Последовательное выполнение команд                                     | ✅ полностью                                       | C, Pascal, BASIC                     | `python\ndef greet(name):\n    print(f"Hello, {name}")\ngreet("Alice")`                                                                                                                     |
| **Функциональное**                 | Программы строятся из чистых функций, которые не изменяют состояние                                 | - Чистые функции (без побочных эффектов)<br>- Иммутабельные данные<br>- Использование `map`, `reduce`, `filter`<br>- Функции как объекты первого класса<br>- Рекурсия вместо циклов | ✅ частично                                        | Haskell, Erlang, Clojure, F#         | `python\nfrom functools import reduce\nnums = [1,2,3,4]\nsquared = list(map(lambda x: x**2, nums))\nsum_total = reduce(lambda a,b: a+b, nums)`                                              |
| **Объектно-ориентированное (OOP)** | Программа состоит из объектов, которые инкапсулируют данные и методы                                | - Классы и объекты<br>- Инкапсуляция (private/public через соглашение `_`)<br>- Наследование и полиморфизм<br>- Абстракция и интерфейсы<br>- Взаимодействие через методы            | ✅ полностью                                       | Java, C++, Python, C#                | `python\nclass Person:\n    def __init__(self, name):\n        self.name = name\n    def greet(self):\n        print(f"Hello, {self.name}")\np = Person("Alice")\np.greet()`                |
| **Логическое**                     | Программа описывает правила и факты, а выполнение — поиск выводов                                   | - Факты и правила<br>- Вывод на основе логических выражений<br>- Декларативное описание задач                                                                                       | ❌ нет нативно                                     | Prolog                               | —                                                                                                                                                                                           |
| **Декларативное**                  | Программа описывает *что* нужно сделать, а не *как*                                                 | - Фокус на описании результата<br>- Минимум инструкций управления потоком<br>- Часто используется в SQL, HTML, CSS                                                                  | ✅ частично                                        | SQL, HTML, Haskell                   | `python\nnums = [1,2,3,4,5]\neven = [x for x in nums if x%2==0]`                                                                                                                            |
| **Событийно-ориентированное**      | Программа реагирует на события (клики, сообщения, таймеры)                                          | - Определение обработчиков событий<br>- Цикл событий (event loop)<br>- Асинхронная обработка                                                                                        | ✅ через `asyncio`, Tkinter, PyQt, pygame          | JavaScript, Node.js, C#              | `python\nimport asyncio\nasync def say_hello():\n    print('Hello')\nasyncio.run(say_hello())`                                                                                              |
| **Параллельное / Конкурентное**    | Программа выполняется одновременно в нескольких потоках или процессах                               | - Разделение задач (threads, processes)<br>- Синхронизация доступа к данным<br>- Избежание гонок и дедлоков                                                                         | ✅ через `threading`, `multiprocessing`, `asyncio` | Go, Erlang, Rust, Java               | `python\nfrom threading import Thread\n\ndef worker():\n    print("Working")\nthreads = [Thread(target=worker) for _ in range(3)]\nfor t in threads: t.start()\nfor t in threads: t.join()` |
| **Компонентное / Модульное**       | Программа состоит из независимых модулей или компонентов                                            | - Чёткое разделение модулей<br>- Интерфейсы для взаимодействия<br>- Переиспользуемость и тестируемость                                                                              | ✅ полностью (модули, пакеты)                      | Java (Spring), Python (packages), C# | `python\n# module.py\nPI = 3.14\ndef area(r):\n    return PI * r**2\n\n# main.py\nfrom module import area\nprint(area(5))`                                                                  |

'''
#Рекурсия:
'''
Python's default recursion limit is 1000, 
which prevents infinite recursion from crashing the program by overwhelming the call stack. 
This limit can be increased using the sys.setrecursionlimit() function, 
though this should be done carefully to avoid memory overflow errors.
'''



def rec_function(param):
    if base_case_reached: #Base Case
        return final_result
    else:
        return rec_function(new_param) #Recursive Case
    

def fib(num):
    if num <= 1:
        return num
    else:
        result = fib(num - 1) + fib(num - 2)
        return result

print("Summ of series: ", fib(3))
'''
→ fib(3)
  → fib(2)
    → fib(1)
    ← возвращаем 1 (базовый случай)
    → fib(0)
    ← возвращаем 0 (базовый случай)
  ← fib(2) = 1 + 0 = 1
  → fib(1)
  ← возвращаем 1 (базовый случай)
← fib(3) = 1 + 1 = 2
Result: 2
'''

def fib_position(pos):
    if pos == 1:
        return 0
    elif pos == 2:
        return 1
    elif pos == 3:
        return 1
    elif pos == 4:
        return 2
    else:
        # Должна вызывать саму себя!
        result = fib_position(pos - 1) + fib_position(pos - 2)
        return result

print("Number in position: ", fib_position(3))  # Должно вернуть 1

def fib_position1(pos):
    """Стандартная последовательность: 0, 1, 1, 2, 3, 5, ..."""
    if pos == 1:
        return 0
    elif pos == 2:
        return 1
    else:
        return fib_position1(pos - 1) + fib_position1(pos - 2)

# Проверка:
for i in range(1, 10):
    print(f"Позиция {i}: {fib_position1(i)}")




# Lists
l1 = [1,[1,2,3],[1,[1,2]]]

# calc sum of nested lists recursively
def sum_nested_list(lst, index = 0):
    # ↓↓↓ БАЗОВЫЕ СЛУЧАИ (остановка рекурсии) ↓↓↓
    if not lst:  #Base Case - пустой список
        return 0
    
    if index >= len(lst):  #Base Case - дошли до конца
        return 0
    
    # ↓↓↓ РЕКУРСИВНЫЕ СЛУЧАИ (продолжение рекурсии) ↓↓↓
    current_element = lst[index]
    
    if isinstance(current_element, int):  #Recursive Case
        return current_element + sum_nested_list(lst, index + 1)
    elif isinstance(current_element, list):  #Recursive Case
        return sum_nested_list(current_element, 0) + sum_nested_list(lst, index + 1)
    else: #Recursive Case
        return sum_nested_list(lst, index + 1)


print("Sum:", sum_nested_list(l1))
'''
sum_nested_list([1,[1,2,3],[1,[1,2]]], index=0)
│
├─ index=0 < len=3 → продолжаем
├─ current_element = 1 (число)
├─ РЕКУРСИВНЫЙ СЛУЧАЙ: число
│  → return 1 + sum_nested_list(lst, index=1)
│     │
│     └─ sum_nested_list([1,[1,2,3],[1,[1,2]]], index=1)
│        │
│        ├─ index=1 < len=3 → продолжаем
│        ├─ current_element = [1,2,3] (список)
│        ├─ РЕКУРСИВНЫЙ СЛУЧАЙ: список
│        │  → return sum_nested_list([1,2,3], 0) + sum_nested_list(lst, index=2)
│        │     │
│        │     ├─ ЛЕВАЯ ВЕТКА: sum_nested_list([1,2,3], 0)
│        │     │  │
│        │     │  ├─ index=0 < len=3 → продолжаем
│        │     │  ├─ current_element = 1 (число)
│        │     │  ├─ return 1 + sum_nested_list([1,2,3], 1)
│        │     │  │     │
│        │     │  │     └─ sum_nested_list([1,2,3], 1)
│        │     │  │        │
│        │     │  │        ├─ index=1 < len=3 → продолжаем
│        │     │  │        ├─ current_element = 2 (число)
│        │     │  │        ├─ return 2 + sum_nested_list([1,2,3], 2)
│        │     │  │        │     │
│        │     │  │        │     └─ sum_nested_list([1,2,3], 2)
│        │     │  │        │        │
│        │     │  │        │        ├─ index=2 < len=3 → продолжаем
│        │     │  │        │        ├─ current_element = 3 (число)
│        │     │  │        │        ├─ return 3 + sum_nested_list([1,2,3], 3)
│        │     │  │        │        │     │
│        │     │  │        │        │     └─ sum_nested_list([1,2,3], 3)
│        │     │  │        │        │        │
│        │     │  │        │        │        ├─ БАЗОВЫЙ СЛУЧАЙ: index=3 >= len=3
│        │     │  │        │        │        └─ return 0
│        │     │  │        │        │
│        │     │  │        │        └─ → 3 + 0 = 3
│        │     │  │        │
│        │     │  │        └─ → 2 + 3 = 5
│        │     │  │
│        │     │  └─ → 1 + 5 = 6  ← РЕЗУЛЬТАТ ЛЕВОЙ ВЕТКИ
│        │     │
│        │     └─ ПРАВАЯ ВЕТКА: sum_nested_list(lst, index=2)
│        │        │
│        │        └─ sum_nested_list([1,[1,2,3],[1,[1,2]]], index=2)
│        │           │
│        │           ├─ index=2 < len=3 → продолжаем
│        │           ├─ current_element = [1,[1,2]] (список)
│        │           ├─ РЕКУРСИВНЫЙ СЛУЧАЙ: список
│        │           │  → return sum_nested_list([1,[1,2]], 0) + sum_nested_list(lst, index=3)
│        │           │     │
│        │           │     ├─ ЛЕВАЯ ВЕТКА: sum_nested_list([1,[1,2]], 0)
│        │           │     │  │
│        │           │     │  ├─ index=0 < len=2 → продолжаем
│        │           │     │  ├─ current_element = 1 (число)
│        │           │     │  ├─ return 1 + sum_nested_list([1,[1,2]], 1)
│        │           │     │  │     │
│        │           │     │  │     └─ sum_nested_list([1,[1,2]], 1)
│        │           │     │  │        │
│        │           │     │  │        ├─ index=1 < len=2 → продолжаем
│        │           │     │  │        ├─ current_element = [1,2] (список)
│        │           │     │  │        ├─ return sum_nested_list([1,2], 0) + sum_nested_list([1,[1,2]], 2)
│        │           │     │  │        │     │
│        │           │     │  │        │     ├─ ЛЕВАЯ: sum_nested_list([1,2], 0)
│        │           │     │  │        │     │  │
│        │           │     │  │        │     │  ├─ index=0 < len=2 → продолжаем
│        │           │     │  │        │     │  ├─ current_element = 1 (число)
│        │           │     │  │        │     │  ├─ return 1 + sum_nested_list([1,2], 1)
│        │           │     │  │        │     │  │     │
│        │           │     │  │        │     │  │     └─ sum_nested_list([1,2], 1)
│        │           │     │  │        │     │  │        │
│        │           │     │  │        │     │  │        ├─ index=1 < len=2 → продолжаем
│        │           │     │  │        │     │  │        ├─ current_element = 2 (число)
│        │           │     │  │        │     │  │        ├─ return 2 + sum_nested_list([1,2], 2)
│        │           │     │  │        │     │  │        │     │
│        │           │     │  │        │     │  │        │     └─ sum_nested_list([1,2], 2)
│        │           │     │  │        │     │  │        │        │
│        │           │     │  │        │     │  │        │        ├─ БАЗОВЫЙ СЛУЧАЙ: index=2 >= len=2
│        │           │     │  │        │     │  │        │        └─ return 0
│        │           │     │  │        │     │  │        │
│        │           │     │  │        │     │  │        └─ → 2 + 0 = 2
│        │           │     │  │        │     │  │
│        │           │     │  │        │     │  └─ → 1 + 2 = 3
│        │           │     │  │        │     │
│        │           │     │  │        │     └─ ПРАВАЯ: sum_nested_list([1,[1,2]], 2)
│        │           │     │  │        │        │
│        │           │     │  │        │        ├─ БАЗОВЫЙ СЛУЧАЙ: index=2 >= len=2
│        │           │     │  │        │        └─ return 0
│        │           │     │  │        │
│        │           │     │  │        └─ → 3 + 0 = 3
│        │           │     │  │
│        │           │     │  └─ → 1 + 3 = 4  ← РЕЗУЛЬТАТ ЛЕВОЙ ВЕТКИ
│        │           │     │
│        │           │     └─ ПРАВАЯ ВЕТКА: sum_nested_list(lst, index=3)
│        │           │        │
│        │           │        ├─ БАЗОВЫЙ СЛУЧАЙ: index=3 >= len=3
│        │           │        └─ return 0
│        │           │
│        │           └─ → 4 + 0 = 4  ← РЕЗУЛЬТАТ ПРАВОЙ ВЕТКИ
│        │
│        └─ → 6 + 4 = 10  ← РЕЗУЛЬТАТ ДЛЯ index=1
│
└─ → 1 + 10 = 11  ← ФИНАЛЬНЫЙ РЕЗУЛЬТАТ
'''

# ======================================================
#TODO: 📝 Практика: рекурсия в Python
# ======================================================

##✅TODO: 1. Факториал
# Реализуй функцию factorial(n), которая вычисляет факториал числа n.
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else: 
        return n * factorial(n - 1)

print(factorial(5)) 

##✅TODO: 2. Фибоначчи
# Реализуй функцию fibonacci(n), которая возвращает n-е число Фибоначчи.
def fibonacci(n):
    if n <= 1: return n
    else: return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(5))


##TODO: 3. Сумма элементов списка
# Напиши функцию recursive_sum(lst), которая возвращает сумму элементов списка.
def recursive_sum(lst):
    pass


##TODO: 4. Степень числа
# Реализуй функцию power(base, exp), которая вычисляет base^exp рекурсивно.
def power(base, exp):
    pass


##TODO: 5. Разворот строки
# Напиши функцию reverse_string(s), которая разворачивает строку.
def reverse_string(s):
    pass


##TODO: 6. Проверка палиндрома
# Напиши функцию is_palindrome(s), которая проверяет, является ли строка палиндромом.
def is_palindrome(s):
    pass


##TODO: 7. Поиск максимального элемента в списке
# Напиши функцию recursive_max(lst), которая ищет максимум в списке рекурсивно.
def recursive_max(lst):
    pass


##TODO: 8. Сумма цифр числа
# Напиши функцию digit_sum(n), которая возвращает сумму цифр числа n.
def digit_sum(n):
    pass


##TODO: 9. Бинарный поиск
# Напиши функцию binary_search(lst, target, left, right), которая ищет target рекурсивно.
def binary_search(lst, target, left, right):
    pass


##TODO: 10. Ханойские башни
# Реализуй функцию hanoi(n, source, target, auxiliary),
# которая печатает шаги для перемещения n дисков.
def hanoi(n, source, target, auxiliary):
    pass


# ======================================================
# 🔥 Попробуй написать эти функции и проверить результат!
# ======================================================


#Scopes

'''
Python ищет переменные по правилу LEGB:

L (Local) — локальная область функции
E (Enclosing) — область внешних функций (замыкания)
G (Global) — глобальная область модуля
B (Built-in) — встроенные имена Python (len, print, range и т.д.)

Local → Enclosing → Global → Built-in

'''
# 📌 Шпаргалка по областям видимости в Python (LEGB)
# Local → Enclosing → Global → Built-in

# --- Global (глобальная область) ---
x = "global"  # переменная доступна во всём модуле

def show_global():
    print(x)  # ищет в Global → "global"

show_global()


# --- Local (локальная область) ---
def local_scope():
    y = "local"  # локальная переменная функции
    print(y)     # Local

local_scope()


# --- Enclosing (замыкания / область внешней функции) ---
def outer():
    z = "enclosing"  # переменная во внешней функции
    def inner():
        print(z)     # Enclosing
    inner()

outer()


# --- Built-in (встроенные имена) ---
print(len([1, 2, 3]))  # Built-in функция len → 3

# можно перекрыть встроенное имя:
len = 42
print(len)  # теперь это переменная, а не функция


# --- Использование global ---
count = 0

def increment():
    global count   # явно говорим: использовать глобальную переменную
    count += 1

increment()
print(count)  # 1


# --- Использование nonlocal ---
def outer_func():
    value = 0
    def inner_func():
        nonlocal value  # ищет в Enclosing, а не в Global
        value += 1
        print(value)
    inner_func()

outer_func()  # 1
'''
# Python ищет переменные в порядке:
#
# Local (локальная функция)
#   ↓
# Enclosing (область внешних функций / замыкания)
#   ↓
# Global (глобальная область текущего модуля)
#   ↓
# Built-in (встроенные имена Python)
#
# ┌───────────────────────────────┐
# │ Built-in (len, print, range)  │
# └───────────────▲───────────────┘
#                 │
# ┌───────────────┴───────────────┐
# │ Global (переменные модуля)    │
# └───────────────▲───────────────┘
#                 │
# ┌───────────────┴───────────────┐
# │ Enclosing (замыкания)         │
# └───────────────▲───────────────┘
#                 │
# ┌───────────────┴───────────────┐
# │ Local (переменные функции)    │
# └───────────────────────────────┘
'''
# L - Local (локальная)
# E - Enclosing (охватывающая) 
# G - Global (глобальная)
# B - Built-in (встроенная)

global_var = "global"          # ← Global scope

def outer():
    enclosing_var = "enclosing" # ← Enclosing scope
    
    def inner():
        local_var = "local"    # ← Local scope
        print(local_var)       # ✅ Local → Local
        print(enclosing_var)   # ✅ Local → Enclosing  
        print(global_var)      # ✅ Local → Global
        print(len)             # ✅ Local → Built-in
    
    return inner
# ======================================================
#TODO: 📝 Практика: области видимости (LEGB) в Python
# ======================================================

##✅TODO: 1. Local
# Напиши функцию square(x), которая возвращает квадрат числа.
def square(k):
    return k ** 2
print(square(2))
# Проверь, что переменная x недоступна вне функции.
try:
    print(k)
except NameError:
    print("Переменная k недоступна вне функции") 


##TODO: 2. Global
# Создай глобальную переменную counter = 0
# и функцию increment(), которая увеличивает её на 1.
counter = 0
def increment():
    pass


##TODO: 3. Ошибка без global
# Попробуй сделать x = x + 1 без global и посмотри на ошибку.
x = 5
def wrong_increment():
    pass


##TODO: 4. Enclosing
# Функция outer() создаёт переменную msg,
# а вложенная inner() печатает её.
def outer():
    pass


##TODO: 5. nonlocal
# Переделай outer() так, чтобы inner() меняла msg.
def outer2():
    pass


##✅TODO: 6. Built-in
# Создай переменную len = 100 и попробуй вызвать len([1,2,3]).
# Объясни, что произошло.
len = 100
len([1,2,3]) #TypeError: 'int' object is not callable
#мы переопределили встроенную функцию и теперь пытаемся её использовать как раньше. Теперь э то переменная которую мы не можем вызвать как функцию


##TODO: 7. Замыкание (closure)
# Функция make_multiplier(n) должна возвращать вложенную функцию,
# которая умножает число на n.
def make_multiplier(n):
    pass


##TODO: 8. Глобальный и локальный с одинаковым именем
# Создай глобальную переменную name = "Global"
# и функцию, в которой name = "Local".
# Проверь, что выводится внутри и снаружи функции.


##TODO: 9. Несколько уровней Enclosing
# Сделай 3 вложенные функции и проброс

#TODO: 📝 Практика: first-class citizen
# =============================================================================
# FIRST-CLASS CITIZEN (ОБЪЕКТЫ ПЕРВОГО КЛАССА) В PYTHON
# 
# Кратко: Функции - это объекты, с которыми можно работать как с любыми другими 
# данными (числами, строками, списками)
# 
# ОСНОВНЫЕ ВОЗМОЖНОСТИ:
# - Присваивание функций переменным
# - Передача функций как аргументов в другие функции  
# - Возвращение функций из функций
# - Хранение функций в структурах данных
# =============================================================================

# 📍 1. ПРИСВАИВАНИЕ ФУНКЦИЙ ПЕРЕМЕННЫМ
# (используется для создания псевдонимов, динамического выбора реализаций)
def greet(name):
    return f"Hello, {name}"

my_function = greet  # Присваиваем функцию переменной
print(my_function("Alice"))  # Вызываем через переменную

# 📍 2. ПЕРЕДАЧА ФУНКЦИЙ КАК АРГУМЕНТОВ
# (используется в колбэках, функциях высшего порядка, обработчиках событий)
def process_numbers(numbers, operation):
    """Функция высшего порядка - принимает другую функцию как аргумент"""
    return [operation(x) for x in numbers]

def square(x):
    return x * x

result = process_numbers([1, 2, 3], square)  # Передаем функцию как аргумент
print(result)  # [1, 4, 9]

# 📍 3. ВОЗВРАЩЕНИЕ ФУНКЦИЙ ИЗ ФУНКЦИЙ
# (используется в замыканиях, фабриках функций, декораторах)
def create_multiplier(factor):
    """Фабрика функций - возвращает новую функцию"""
    def multiplier(x):
        return x * factor
    return multiplier

double = create_multiplier(2)  # Получаем функцию из функции
triple = create_multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15

# 📍 4. ХРАНЕНИЕ ФУНКЦИЙ В СТРУКТУРАХ ДАННЫХ
# (используется для стратегий, плагинов, роутинга, командных паттернов)
# Словарь стратегий
operations = {
    'add': lambda x, y: x + y,
    'subtract': lambda x, y: x - y,
    'multiply': lambda x, y: x * y
}

# Выбор и вызов функции по ключу
operation = operations['add']
result = operation(10, 5)  # 15

# Список обработчиков
'''
middleware = [log_request, authenticate, validate_data]
for handler in middleware:
    handler(request)
'''

# =============================================================================
# ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ FIRST-CLASS FUNCTIONS:
# 
# 1. ДЕКОРАТОРЫ - функции, принимающие и возвращающие функции
# 2. КОЛБЭКИ - функции, передаваемые для обратного вызова
# 3. СТРАТЕГИИ - выбор алгоритма из набора функций
# 4. ОБРАБОТЧИКИ СОБЫТИЙ - регистрация функций-обработчиков
# 5. PLUGIN SYSTEMS - динамическая загрузка функциональности
# 6. TEСТИРОВАНИЕ - подмена реальных функций mock-объектами
# 7. АСИНХРОННОЕ ПРОГРАММИРОВАНИЕ - передача корутин
# =============================================================================

# 📍 ПРИМЕР: СИСТЕМА ПЛАГИНОВ С ФУНКЦИЯМИ ПЕРВОГО КЛАССА
plugins = {}

def register_plugin(name):
    """Декоратор для регистрации плагинов"""
    def decorator(func):
        plugins[name] = func
        return func
    return decorator

@register_plugin('json_parser')
def parse_json(data):
    return f"Parsed JSON: {data}"

@register_plugin('xml_parser')  
def parse_xml(data):
    return f"Parsed XML: {data}"

# Использование зарегистрированных плагинов
data = "some_data"
parser = plugins['json_parser']  # Получаем функцию из словаря
result = parser(data)  # Вызываем полученную функцию

# =============================================================================
# ВАЖНО: Благодаря first-class functions Python поддерживает 
# функциональное программирование и позволяет создавать гибкие, 
# расширяемые архитектуры с высоким уровнем абстракции.
# =============================================================================

##✅TODO:📍 Присваивание функций переменным
# Создайте несколько функций (сложение, умножение) и присвойте их переменным
def sum(a,b):
    return a + b
def multiply(a,b):
    return a * b
sum1 = sum
multiply1 = multiply
print(type(sum1), type(multiply1))


##✅TODO: 📍 Передача функций как аргументов
# Напишите функцию-калькулятор, которая принимает операцию как аргумент
def calc(a,b,action):
    match action:
        case 'add':
            return a+b
        case 'sub':
            return a-b
        case 'multi':
            return a*b
        case 'div':
            if b == 0: return "Error: ZeroDivisionError"
            return a/b
        case _: return "Not correct action"
# Примеры использования
print(calc(10, 5, 'add'))    # 15
print(calc(10, 5, 'sub'))    # 5
print(calc(10, 5, 'multi'))  # 50
print(calc(10, 5, 'div'))    # 2.0
print(calc(10, 0, 'div'))    # Ошибка: деление на 0
print(calc(10, 5, 'mod'))    # Неверная операция

##✅TODO:📍 Возвращение функций из функций
# Создайте функцию-генератор математических операций
def math_generator(operation):
    if operation.lower() == 'sum':
        def sum(x,y):
            return x+y
        return sum 

sum1 = math_generator('sum')  
print('label1: ', sum1(2,5))                   
    

##TODO: 📍 Хранение функций в структурах данных
# Создайте словарь с функциями-операциями и список с функциями-валидаторами
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def multi(x, y):
    return x * y

def div(x, y):
    if y == 0:
        return "Ошибка: деление на 0"
    return x / y

operations = {
    'sum':sum,
    'sub':sub,
    'multi':multi,
    'div':div
}
def int_valid(x):
    return isinstance(x, int)

def str_valid(x):
    return isinstance(x, str)

def float_valid(x):
    return isinstance(x, float)

def dict_valid(x):
    return isinstance(x, dict)

validators = [
    int_valid,
    str_valid,
    float_valid,
    dict_valid
]
x, y = 5, 3
op = operations['sum']  # add
print(op(x, y))     # 8

value = 10
for validator in validators:
    print(validator(value)) 

##TODO: 📍 Функции как элементы классов
# Создайте класс, где методы можно динамически подменять

##TODO: 📍 Функции высшего порядка
# Реализуйте map, filter, reduce своими руками

##TODO: 📍 Композиция функций
# Напишите функцию-композитор, которая объединяет несколько функций

##TODO: 📍 Динамический выбор функций
# Создайте систему плагинов, где функции выбираются по имени

##TODO: 📍 Функции как параметры конфигурации
# Реализуйте настройку поведения через передачу функций

##TODO: 📍 Колбэк-функции
# Создайте систему событий с регистрацией обработчиков

##TODO: 📍 Замыкания (closures)
# Напишите функцию-счетчик и функцию-мультипликатор с запоминанием состояния

##TODO: 📍 Декораторы как first-class функций
# Создайте параметризуемый декоратор для логирования и кэширования

##TODO: 📍 Функциональное программирование
# Реализуйте каррирование и частичное применение функций

##TODO: 📍 Функции в многопоточности
# Передавайте функции в потоки и пулы процессов

##TODO: 📍 Сериализация функций
# Создайте систему сохранения и восстановления состояний функций

#TODO: 📝 Практика: Closure - замыкания
##TODO: 📍 Базовые замыкания
# Создайте функцию-счетчик, которая запоминает свое состояние между вызовами

##TODO: 📍 Замыкания с параметрами
# Создайте функцию-мультипликатор, которая запоминает множитель

##TODO: 📍 Замыкания для конфигурации
# Создайте функцию-форматер, которая запоминает шаблон вывода

##TODO: 📍 Замыкания с изменяемым состоянием
# Создайте функцию-буфер, которая накапливает данные между вызовами

##TODO: 📍 Замыкания для мемоизации
# Создайте функцию-кэш, которая запоминает результаты вычислений

##TODO: 📍 Замыкания в циклах
# Создайте несколько функций в цикле, каждая запоминает свой индекс

##TODO: 📍 Замыкания с доступом на запись
# Создайте функцию-кошелек с методами пополнения и списания

##TODO: 📍 Замыкания для создания API
# Создайте функцию-конструктор объектов с приватными методами

##TODO: 📍 Замыкания с несколькими уровнями
# Создайте вложенные замыкания с разными контекстами

##TODO: 📍 Замыкания для потокобезопасности
# Создайте функцию-синхронизатор с внутренним состоянием

##TODO: 📍 Замыкания с лямбда-функциями
# Создайте замыкание, возвращающее лямбду с доступом к внешнему scope

##TODO: 📍 Замыкания для декораторов
# Реализуйте декоратор через замыкание с параметрами

##TODO: 📍 Замыкания с обработчиками событий
# Создайте систему подписки на события с сохранением контекста

##TODO: 📍 Замыкания для тестирования
# Создайте функцию-мок с запоминанием истории вызовов

##TODO: 📍 Замыкания с очисткой ресурсов
# Создайте функцию с внутренними ресурсами и методом cleanup

#TODO: 📝 Практика: __closure__ - Enclosing content
'''
Enclosing content — это механизм, позволяющий внутренним функциям 
получать доступ к переменным внешних функций, 
что является основой для замыканий и многих продвинутых паттернов в Python.

🎪 Когда используется Enclosing Scope:
Замыкания (Closures)
Декораторы
Фабрики функций
Сохранение состояния
Создание API с приватными данными
'''
##TODO: 📍 Исследование атрибута __closure__
# Создайте замыкание и изучите его атрибут __closure__

##TODO: 📍 Доступ к переменным из __closure__
# Получите значения захваченных переменных через cell_contents

##TODO: 📍 Сравнение __closure__ разных функций
# Создайте несколько замыканий и сравните их атрибуты __closure__

##TODO: 📍 Замыкания без __closure__
# Создайте функцию, которая не захватывает переменные и проверьте __closure__

##TODO: 📍 Изменение захваченных переменных
# Попробуйте изменить значения в cell_contents и отследите поведение

##TODO: 📍 __closure__ в лямбда-функциях
# Создайте лямбду с захватом переменных и изучите ее __closure__

##TODO: 📍 __closure__ в декораторах
# Исследуйте атрибут __closure__ у функций, обернутых декораторами

##TODO: 📍 Цепочка замыканий
# Создайте вложенные замыкания и изучите их __closure__ атрибуты

##TODO: 📍 __closure__ и garbage collection
# Исследуйте, как __closure__ влияет на сборку мусора

##TODO: 📍 Модификация __closure__
# Попробуйте динамически изменить атрибут __closure__ функции

##TODO: 📍 __closure__ в методах класса
# Создайте замыкание внутри метода класса и изучите его __closure__

##TODO: 📍 Сравнение __closure__ и __globals__
# Исследуйте разницу между захваченными и глобальными переменными

##TODO: 📍 __closure__ в генераторах
# Создайте генератор с захватом переменных и изучите его __closure__

##TODO: 📍 Визуализация __closure__
# Напишите функцию для красивого вывода информации о замыкании

##TODO: 📍 Практическое использование __closure__
# Реализуйте мемоизацию с ручным управлением через __closure__

#TODO: 📝 Практика: Decorators - декораторы
'''
✅ ЦЕЛЕСООБРАЗНО:
Логирование и мониторинг
Кэширование результатов
Аутентификация и авторизация
Валидация входных данных
Обработка ошибок и повторные попытки
Измерение производительности
Транзакции БД
Rate limiting (ограничение частоты запросов)

❌ НЕ ЦЕЛЕСООБРАЗНО:
Для простых функций, которые вызываются 1-2 раза
Когда логика слишком тесно связана с бизнес-правилами
Если декоратор делает код менее читаемым
Для критичных к производительности участков кода

Декораторы целесообразно использовать для сквозной функциональности (cross-cutting concerns), 
когда нужно добавить поведение к нескольким функциям без дублирования кода и нарушения 
принципа DRY (Don't Repeat Yourself).
Используйте умеренно и только когда это улучшает читаемость и поддерживаемость кода!
'''
#TODO: 📍 Базовые декораторы
#✅TODO: Создайте декоратор для измерения времени выполнения функции
'''
from datetime import datetime

def decorator1(func):
    
    def wrapper(*args, **kwargs):
        time_from = datetime.now()
        
        result = func(*args, **kwargs)
        
        time_to = datetime.now()
        elapsed = (time_to - time_from).total_seconds() * 1000 
        print(f"Время выполнения {func.__name__}: {elapsed:.3f} ms")
        return result
    return wrapper
    
@decorator1
def func1(num):
    return num ** 1000
    
print(func1(10))
'''

##✅TODO: 📍 Декораторы с аргументами
# Создайте параметризуемый декоратор для повторного выполнения функции
'''
def repeat_dec(n): # <- декоратор с аргументом
    def print_dec(func):
        def wrapper(*args, **kwargs):
            for i in range(n): # повторяем n раз
                x, y = args
                print(f"Sum of {x} and {y} = {func(*args, **kwargs)}")
        return wrapper
    return print_dec

@repeat_dec(3)# повторим 3 раза
def func2(x,y):
    return x+y

func2(1,2)
'''

##TODO:📍 Декораторы методов класса
# Создайте декоратор для логирования вызовов методов класса

##✅TODO: 📍 Декораторы с сохранением метаданных
# Импортируйте functools.wraps, чтобы сохранить исходное имя функции и строку документации @functools.wraps(func)
# Реализуйте декоратор, который сохраняет __name__ и __doc__ оригинальной функции
from functools import wraps
def dec(func):
    @wraps(func)
    def wrap():
        print(f"Name: {func.__name__}, Docs: {func.__doc__}") #тут OK если без @wraps(func)
        func()
    return wrap

@dec
def f2():
    """_summary_
    """
    print("Hello")
    
f2()
f2()
print(f2.__name__)  # wrap если без @wraps(func)
print(f2.__doc__)   # None если без @wraps(func)
    
##✅TODO: 📍 Несколько декораторов на одной функции
# Создайте комбинацию декораторов: кэширование + логирование + валидация
'''
from functools import wraps
def cache_dec(func):
    """Cache doc
    """
    cache = {} # 1. Создаём словарь для хранения результатов
    @wraps(func)
    def wrap(*args, **kwargs):
        key = (args, tuple(kwargs.items())) # 2. Генерируем ключ из аргументов
        if key in cache: # 3. Проверяем, есть ли результат в кэше
            print(f"cache hit for key {key}")
            return cache[key]  # 4. Если есть, возвращаем его
        result = func(*args, **kwargs) # 5. Если нет, вызываем функцию
        cache[key] = result # 6. Сохраняем результат в кэше
        return result  # 7. Возвращаем результат
    return wrap

def logging_dec(func):
    """logging doc
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args} ang kwargs={kwargs}, {func.__doc__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned result: {result}")
        return result
    return wrap

def validation_dec(func):
    """Validation doc
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        if not isinstance(result, (int, float)):
            raise ValueError("Result must be a number")
        return result
    return wrap

# Комбинация декораторов
@cache_dec
@logging_dec
@validation_dec
def my_func(x, y, *args, **kwargs):
    """Func1 doc
    """
    return x + y

print(my_func(2, 3, a=2)) #Calling wrap with args=(2, 3) ang kwargs={}
print(my_func(2, 3, a=2))  # сработает кэш
'''
##TODO: 📍 Декораторы с доступом к аргументам
# Создайте декоратор, который проверяет типы аргументов функции

##TODO: 📍 Класс-декоратор
# Реализуйте декоратор в виде класса с методами __call__ и __init__

##TODO: 📍 Декораторы для свойств класса
# Создайте декоратор @property с дополнительной логикой валидации

##TODO: 📍 Декораторы с состоянием
# Создайте декоратор, который подсчитывает количество вызовов функции

##TODO: 📍 Декораторы для регистрации функций
# Создайте декоратор, который автоматически регистрирует функции в словаре

##TODO: 📍 Декораторы с условием применения
# Создайте декоратор, который применяется только при определенных условиях

##TODO: 📍 Декораторы для обработки исключений
# Создайте декоратор с повторными попытками при возникновении ошибок

##TODO: 📍 Декораторы модификации возвращаемого значения
# Создайте декоратор, который преобразует результат функции

##TODO: 📍 Декораторы для кэширования
# Реализуйте декоратор @cache с ограничением по размеру и времени

##TODO: 📍 Декораторы с настройкой через конфиг
# Создайте декоратор, который читает настройки из внешнего конфигурационного файла

