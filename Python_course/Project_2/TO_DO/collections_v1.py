"""
КОМПРЕХЕНСИВНАЯ ШПАРГАЛКА ПО COLLECTIONS В PYTHON
Set vs Frozenset vs Tuple vs List vs Dict
"""

# ==================== SET (МНОЖЕСТВО) ====================
# - Изменяемый (mutable)
# - Неупорядоченный (unordered) 
# - Только уникальные элементы (no duplicates)
# - Только хешируемые элементы (hashable items only)
# - Поддерживает математические операции над множествами

my_set = {1, 2, 3, 2, 1}  # {1, 2, 3} - дубликаты автоматически удаляются

# МЕТОДЫ РАБОТЫ С ЭЛЕМЕНТАМИ:
my_set.add(4)              # ✅ Добавить один элемент: {1, 2, 3, 4}
my_set.update([5, 6, 7])   # ✅ Добавить несколько элементов: {1, 2, 3, 4, 5, 6, 7}
my_set.remove(1)           # ✅ Удалить элемент (KeyError если нет): {2, 3, 4, 5, 6, 7}
my_set.discard(10)         # ✅ Удалить элемент (без ошибки если нет): {2, 3, 4, 5, 6, 7}
my_set.pop()               # ✅ Удалить и вернуть случайный элемент (т.к. неупорядочен)
my_set.clear()             # ✅ Очистить множество: set()

# МАТЕМАТИЧЕСКИЕ ОПЕРАЦИИ:
set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

set_a | set_b              # ✅ Объединение: {1, 2, 3, 4, 5, 6}
set_a.union(set_b)         # ✅ Альтернатива объединения
set_a & set_b              # ✅ Пересечение: {3, 4}
set_a.intersection(set_b)  # ✅ Альтернатива пересечения
set_a - set_b              # ✅ Разность: {1, 2}
set_a.difference(set_b)    # ✅ Альтернатива разности
set_a ^ set_b              # ✅ Симметрическая разность: {1, 2, 5, 6}
set_a.symmetric_difference(set_b)  # ✅ Альтернатива сим. разности

# ПРОВЕРКИ:
2 in my_set                # ✅ Проверка наличия элемента: True
my_set.isdisjoint({8, 9})  # ✅ Проверка на непересекаемость: True
{1, 2}.issubset({1, 2, 3}) # ✅ Проверка подмножества: True
{1, 2, 3}.issuperset({1, 2}) # ✅ Проверка надмножества: True

# ==================== FROZENSET (НЕИЗМЕНЯЕМОЕ МНОЖЕСТВО) ====================
# - Неизменяемый (immutable)
# - Неупорядоченный (unordered)
# - Только уникальные элементы (no duplicates)
# - Может быть элементом множества/ключом словаря
# - Наследует все методы set кроме изменяющих

fset = frozenset([1, 2, 3, 2, 1])  # frozenset({1, 2, 3})

# МЕТОДЫ (только чтение - те же что у set кроме изменяющих):
fset.union({4, 5})         # ✅ Возвращает новый frozenset: frozenset({1, 2, 3, 4, 5})
fset.intersection({2, 3})  # ✅ Возвращает новый frozenset: frozenset({2, 3})
2 in fset                  # ✅ Проверка наличия: True
len(fset)                  # ✅ Размер: 3

# НЕДОСТУПНЫ (изменяющие методы):
# fset.add(4)              # ❌ AttributeError
# fset.remove(1)           # ❌ AttributeError  
# fset.update([4])         # ❌ AttributeError

# ПРИМЕНЕНИЕ - ключи словаря:
valid_configs = {
    frozenset(['GET', 'POST']): 'read_only',
    frozenset(['GET', 'POST', 'PUT', 'DELETE']): 'full_access'
}

# ==================== TUPLE (КОРТЕЖ) ====================
# - Неизменяемый (immutable) 
# - Упорядоченный (ordered)
# - Разрешает дубликаты (allows duplicates)
# - Может содержать любые типы данных
# - Быстрее list для итераций

my_tuple = (1, 2, 3, "hello", [4, 5], {"key": "value"})

# МЕТОДЫ РАБОТЫ С ЭЛЕМЕНТАМИ (только чтение):
my_tuple[0]                # ✅ Доступ по индексу: 1
my_tuple[1:4]              # ✅ Срез: (2, 3, "hello")
my_tuple.index(2)          # ✅ Поиск индекса элемента: 1
my_tuple.count(2)          # ✅ Подсчет вхождений: 1
3 in my_tuple              # ✅ Проверка наличия: True

# "ИЗМЕНЕНИЕ" ЧЕРЕЗ СОЗДАНИЕ НОВОГО:
new_tuple = my_tuple + (6,)           # ✅ Конкатенация: (1, 2, 3, "hello", [4, 5], {"key": "value"}, 6)
double_tuple = my_tuple * 2           # ✅ Повторение
tuple_from_list = tuple([7, 8, 9])    # ✅ Создание из list

# НЕДОСТУПНЫ (изменяющие методы):
# my_tuple[0] = 10         # ❌ TypeError
# my_tuple.append(6)       # ❌ AttributeError
# my_tuple.remove(1)       # ❌ AttributeError

# ==================== LIST (СПИСОК) - ДЛЯ СРАВНЕНИЯ ====================
# - Изменяемый (mutable)
# - Упорядоченный (ordered)
# - Разрешает дубликаты (allows duplicates)

my_list = [1, 2, 3, 2, 1]

# МЕТОДЫ РАБОТЫ С ЭЛЕМЕНТАМИ:
my_list.append(4)          # ✅ Добавить элемент: [1, 2, 3, 2, 1, 4]
my_list.extend([5, 6])     # ✅ Добавить несколько: [1, 2, 3, 2, 1, 4, 5, 6]
my_list.insert(0, 0)       # ✅ Вставить по индексу: [0, 1, 2, 3, 2, 1, 4, 5, 6]
my_list.remove(2)          # ✅ Удалить первое вхождение: [0, 1, 3, 2, 1, 4, 5, 6]
my_list.pop()              # ✅ Удалить и вернуть последний: 6
my_list.pop(0)             # ✅ Удалить и вернуть по индексу: 0
my_list.clear()            # ✅ Очистить список: []

# ==================== DICT (СЛОВАРЬ) - ДЛЯ СРАВНЕНИЯ ====================
# - Изменяемый (mutable)
# - Упорядоченный (с Python 3.7+)
# - Ключи уникальные и хешируемые
# - Значения любые

my_dict = {'a': 1, 'b': 2, 'c': 3}

# МЕТОДЫ РАБОТЫ С ЭЛЕМЕНТАМИ:
my_dict['d'] = 4           # ✅ Добавить/изменить элемент: {'a':1, 'b':2, 'c':3, 'd':4}
my_dict.update({'e': 5})   # ✅ Обновить несколько: {'a':1, 'b':2, 'c':3, 'd':4, 'e':5}
my_dict.pop('a')           # ✅ Удалить и вернуть значение: 1
my_dict.popitem()          # ✅ Удалить и вернуть последнюю пару: ('e', 5)
del my_dict['b']           # ✅ Удалить элемент
my_dict.clear()            # ✅ Очистить словарь: {}

# ==================== СРАВНЕНИЕ МЕТОДОВ РАБОТЫ С ЭЛЕМЕНТАМИ ====================

"""
✅ ДОБАВЛЕНИЕ ЭЛЕМЕНТОВ:
List:    append(), extend(), insert()
Set:     add(), update()  
Dict:    dict[key] = value, update()
Tuple:   ❌ НЕДОСТУПНО (immutable)
Frozenset: ❌ НЕДОСТУПНО (immutable)

✅ УДАЛЕНИЕ ЭЛЕМЕНТОВ:
List:    remove(), pop(), clear()
Set:     remove(), discard(), pop(), clear()
Dict:    pop(), popitem(), del, clear()
Tuple:   ❌ НЕДОСТУПНО (immutable)
Frozenset: ❌ НЕДОСТУПНО (immutable)

✅ ДОСТУП К ЭЛЕМЕНТАМ:
List:    [index], slice, iteration
Tuple:   [index], slice, iteration  
Set:     iteration only (no index - unordered)
Dict:    [key], iteration over keys/values/items
Frozenset: iteration only (no index - unordered)

✅ ПОИСК ЭЛЕМЕНТОВ:
List:    index(), count(), in operator
Tuple:   index(), count(), in operator
Set:     in operator (very fast - O(1))
Dict:    in operator (checks keys), get()
Frozenset: in operator (very fast - O(1))

✅ МАТЕМАТИЧЕСКИЕ ОПЕРАЦИИ:
Set:     | & - ^ (union, intersection, difference, symmetric_difference)
Frozenset: | & - ^ (return new frozenset)
List:    ❌ НЕТ
Tuple:   ❌ НЕТ  
Dict:    ❌ НЕТ
"""

# ==================== УПРАЖНЕНИЯ ДЛЯ ЗАКРЕПЛЕНИЯ ====================

def exercise_1():
    """Базовые операции с типами коллекций"""
    print("=== Упражнение 1: Базовые операции ===")
    
    # 1. Создайте set из списка с дубликатами
    numbers = [1, 2, 2, 3, 4, 4, 5, 5, 5]
    unique_numbers = None  # Ваш код здесь
    print(f"1. Уникальные числа: {unique_numbers}")
    
    # 2. Создайте frozenset из строки "programming"  
    chars_frozen = None  # Ваш код здесь
    print(f"2. Уникальные символы: {chars_frozen}")
    
    # 3. Создайте tuple с вложенными структурами
    complex_tuple = None  # Ваш код здесь (число, строка, список, множество)
    print(f"3. Сложный кортеж: {complex_tuple}")
    
    # 4. Удалите дубликаты сохраняя порядок (подсказка: dict.fromkeys())
    ordered_unique = None  # Ваш код здесь
    print(f"4. Уникальные с сохранением порядка: {ordered_unique}")

def exercise_2():
    """Операции с множествами"""
    print("\n=== Упражнение 2: Операции с множествами ===")
    
    students_math = {"Alice", "Bob", "Charlie", "Diana"}
    students_physics = {"Bob", "Diana", "Eve", "Frank"}
    
    # 1. Студенты, изучающие оба предмета
    both_subjects = None  # Ваш код здесь
    print(f"1. Оба предмета: {both_subjects}")
    
    # 2. Студенты, изучающие только математику
    only_math = None  # Ваш код здесь
    print(f"2. Только математика: {only_math}")
    
    # 3. Все уникальные студенты
    all_students = None  # Ваш код здесь
    print(f"3. Все студенты: {all_students}")
    
    # 4. Используйте frozenset как ключ словаря
    course_students = {
        None: "Advanced Group"  # Ваш код здесь
    }
    print(f"4. Группы: {course_students}")

def exercise_3():
    """Сравнение методов работы с элементами"""
    print("\n=== Упражнение 3: Сравнение методов ===")
    
    # Данные для экспериментов
    my_list = [1, 2, 3, 4, 5]
    my_set = {1, 2, 3, 4, 5}
    my_tuple = (1, 2, 3, 4, 5)
    my_dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}
    
    # 1. Добавление элемента (где возможно)
    # Ваш код здесь - добавьте 6 в каждую коллекцию где это возможно
    
    # 2. Удаление элемента (где возможно)  
    # Ваш код здесь - удалите 3 из каждой коллекции где это возможно
    
    # 3. Проверка наличия элемента
    contains_3_list = None  # Ваш код здесь
    contains_3_set = None   # Ваш код здесь
    print(f"Поиск элемента 3: list={contains_3_list}, set={contains_3_set}")

def exercise_4():
    """Практические кейсы применения"""
    print("\n=== Упражнение 4: Практические кейсы ===")
    
    # 1. Уникальные посетители сайта (set)
    visitors = ["user1", "user2", "user1", "user3", "user2", "user4"]
    unique_visitors = None  # Ваш код здесь
    print(f"1. Уникальные посетители: {unique_visitors}")
    
    # 2. Конфигурация приложения (frozenset для неизменяемых настроек)
    allowed_methods = None  # Ваш код здесь (frozenset с 'GET', 'POST')
    print(f"2. Разрешенные методы: {allowed_methods}")
    
    # 3. Координаты в пространстве (tuple)
    point_3d = None  # Ваш код здесь (x, y, z)
    print(f"3. Координаты точки: {point_3d}")
    
    # 4. Удаление дубликатов с сохранением порядка
    data_with_duplicates = ["apple", "banana", "apple", "orange", "banana", "grape"]
    unique_ordered = None  # Ваш код здесь
    print(f"4. Уникальные с порядком: {unique_ordered}")

# ==================== РЕШЕНИЯ УПРАЖНЕНИЙ ====================

def solutions():
    """Решения упражнений (раскомментируйте для проверки)"""
    
    # Упражнение 1
    numbers = [1, 2, 2, 3, 4, 4, 5, 5, 5]
    # unique_numbers = set(numbers)
    # chars_frozen = frozenset("programming") 
    # complex_tuple = (1, "hello", [1, 2], {3, 4})
    # ordered_unique = list(dict.fromkeys(numbers))
    
    # Упражнение 2
    students_math = {"Alice", "Bob", "Charlie", "Diana"}
    students_physics = {"Bob", "Diana", "Eve", "Frank"}
    # both_subjects = students_math & students_physics
    # only_math = students_math - students_physics
    # all_students = students_math | students_physics
    # course_students = {frozenset(students_math): "Math Group"}
    
    print("Решения находятся в закомментированном коде")

if __name__ == "__main__":
    # Запустите упражнения для практики:
    # exercise_1()
    # exercise_2() 
    # exercise_3()
    # exercise_4()
    
    # Или посмотрите решения:
    solutions()
    
    print("\n" + "="*50)
    print("КЛЮЧЕВЫЕ ВЫВОДЫ:")
    print("- Set: уникальность + математические операции")
    print("- Frozenset: неизменяемый set (ключи словаря)")
    print("- Tuple: неизменяемый + упорядоченный") 
    print("- List: изменяемый + упорядоченный + дубликаты")
    print("- Dict: пары ключ-значение + уникальные ключи")