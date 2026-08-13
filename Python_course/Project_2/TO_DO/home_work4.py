
# ------------------------------
#✅TODO: Задача 1: Срезы строк
# ------------------------------
import copy


s = "PythonIsFun"

##✅TODO: 1. Получи срез "Python"
print(s[0:6])
##✅TODO: 2. Получи срез "Fun"
print(s[len(s)-3:])
##✅TODO: 3. Получи срез, который состоит из каждого второго символа строки
print(s[1::2])
##✅TODO: 4. Получи срез, который переворачивает строку
print(s[::-1])

# ------------------------------
#✅TODO: Задача 2: Используем find() и index()
# ------------------------------
s2 = "DataScienceIsFun"

##✅TODO: 1. Найди индекс буквы 'S'
s_index = s2.find('S')
print(s2[s_index])
##✅TODO: 2. Найди индекс последней буквы 'n' в строке
n_index = s2.rfind('n')
print(s2[n_index])
##✅TODO: 3. Используй найденные индексы, чтобы получить срез от 'S' до последнего 'n' включительно
print(s2[s_index:n_index+1])
##✅TODO: 4. Попробуй использовать index() вместо find() и сравни результат
s2_index = s2.index('S')
n2_index = s2.rindex('n')
print(s2[s2_index:n2_index+1])
print((s2[s_index:n_index+1] == s2[s2_index:n2_index+1]))

# ------------------------------
#✅TODO: Задача 3: Списки
# ------------------------------
lst = [2, 4, 6, 8, 10, 12, 14]

##✅TODO: 1. Получи срез, содержащий первые 4 элемента
print(lst[0:4])
##✅TODO: 2. Получи срез, содержащий каждый второй элемент, начиная с индекса 1
print(lst[1::2])
##✅TODO: 3. Получи срез списка в обратном порядке
print(lst[::-1])
##✅TODO: 4. Попробуй комбинировать шаг и диапазон, например: каждые два элемента в обратном порядке
print(lst[::-2])

# ------------------------------
#✅TODO: Задача 4: Срезы строк
# ------------------------------
s = "ArtificialIntelligence"

##✅TODO: 1. Получи срез "Intelligence"
# решение:
search_word = 'Intelligence'
print(s[s.rfind(search_word):s.rfind(search_word)+len((search_word)):])

##✅TODO: 2. Получи срез, который состоит из каждого третьего символа строки
# решение:
print(s[2::3])

##✅TODO: 3. Получи срез, который переворачивает слово "Artificial" только
# решение:
search_word = 'Artificial'
word = s[s.rfind(search_word):s.rfind(search_word)+len((search_word)):]
print(word[::-1])


# ------------------------------
#✅TODO: Задача 5: Списки
# ------------------------------
lst = [10, 20, 30, 40, 50, 60, 70, 80]

##✅TODO: 1. Получи срез [30, 40, 50]
# решение:
search_elements = [30, 40, 50]
result_lst = []
for elem in lst:
    if elem in search_elements:
        result_lst.append(elem)
print (result_lst)

##✅TODO: 2. Получи срез [80, 60, 40, 20]
# решение:
search_elements = [80, 60, 40, 20]
result_lst = []
for elem in lst:
    if elem in search_elements:
        result_lst.append(elem)
print (result_lst[::-1])

##✅TODO: 3. Получи срез всех элементов с шагом 3
# решение:
print(lst[::3])

##✅TODO: 4. Попробуй поменять порядок первых 5 элементов на обратный
# решение:
lst1 = lst[:5]
lst2 = lst[5:]
result_lst = lst1[::-1] + lst2
print(result_lst)


# ------------------------------
#✅TODO: Задача 6: Словари + поиск по ключу
# ------------------------------
my_dict = {
    "apple": 10,
    "banana": 5,
    "apricot": 7,
    "grape": 3
}

##✅TODO: 1. Создай список ключей, которые содержат "ap"
# with loop:
keys_with_ap = []
keys = list(my_dict.keys())
for key in keys:
    if 'ap' in key:
        keys_with_ap.append(key)
        
print(keys_with_ap)

#with constructor
keys_with_ap_2 = [k for k in my_dict if 'ap' in k]
print(keys_with_ap_2)

##✅TODO: 2. Создай новый словарь с этими ключами и их значениями
'''
| Способ                                                                      | Что копируется                                         | Глубина                        | Плюсы                                                           | Минусы                                                                                                       |
| --------------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `my_dict.copy()`                                                            | Сам словарь и ссылки на значения                       | Shallow                        | Очень быстрый, простой                                          | Вложенные объекты остаются общими (изменения отражаются в оригинале)                                         |
| `dict(my_dict)`                                                             | То же, что и `.copy()`                                 | Shallow                        | Краткий синтаксис                                               | Тот же недостаток: вложенные mutable объекты общие                                                           |
| `{k: v for k, v in my_dict.items()}`                                        | Ключи и ссылки на значения                             | Shallow                        | Гибкий, можно фильтровать или изменять значения при копировании | Вложенные объекты остаются общими                                                                            |
| `copy.deepcopy(my_dict)`                                                    | Ключи, значения, все вложенные объекты                 | Deep                           | Полная независимость объектов                                   | Медленнее, чем shallow copy; immutable объекты (строки, числа) остаются теми же объектами                    |
| `{k: copy.deepcopy(v) for k, v in my_dict.items()}`                         | Только значения словаря                                | Deep для значений              | Можно оставить ключи без изменений                              | Ключи не копируются; immutable ключи останутся общими                                                        |
| `full_copy(my_dict)` (рекурсивная функция, создаёт новые объекты для всего) | Ключи, значения, все вложенные объекты, даже immutable | Deep (полностью новые объекты) | Полностью независимые объекты, включая строки и числа           | Нужно писать свою функцию, медленнее всех вариантов                                                          |
| `json.loads(json.dumps(my_dict))`                                           | Всё, что сериализуется в JSON                          | Deep                           | Легко для простых структур (числа, строки, списки, словари)     | Не работает с объектами Python, которые нельзя сериализовать в JSON (например, set, пользовательские классы) |

'''
# решение:
my_dict = {
    "int": 42,                               # целое число (immutable)
    "float": 3.14,                           # число с плавающей точкой (immutable)
    "str": "hello",                          # строка (immutable)
    "bool": True,                            # булево значение (immutable)
    "none": None,                            # NoneType (immutable)
    "list": [1, 2, [3, 4]],                  # список (mutable, вложенный список)
    "tuple": (1, 2, (3, 4)),                 # кортеж (immutable, вложенный immutable внутри)
    "tuple2": (1, 2, [3, 4]),                # кортеж (immutable, вложенный mutable внутри)
    "set": {1, 2, 3},                        # множество (mutable)
    "dict": {"a": 1, "b": {"c": 2}},         # вложенный словарь (mutable)
    "bytes": b"bytes",                       # bytes (immutable)
    "bytearray": bytearray(b"bytearray"),    # bytearray (mutable)
    "frozenset": frozenset([1, 2, 3]),       # неизменяемое множество (immutable)
}
#test
def test_copy(original, copied, type_of_copy:str):
    print(type_of_copy)
    for k, v in original.items():
        print(f"\nKey: {k}")
        print("Value equal:", v == copied[k])   # значения совпадают
        print("Different object for mutable?", id(v) != id(copied[k]) if isinstance(v, (dict, list, set)) else "immutable, id not important")
        
        # Для mutable объектов проверяем изменения
        if isinstance(v, list):
            copied[k].append("new")
            print("Original after modifying copy (list):", v)
        if isinstance(v, dict):
            copied[k]["new_key"] = 999
            print("Original after modifying copy (dict):", v)

##✅TODO: Shallow Copy
new_dict = my_dict.copy()
test_copy(my_dict,new_dict,'Shallow Copy: ')
new_dict = dict(my_dict)
test_copy(my_dict,new_dict,'Constructor Shallow Copy: ')
###✅TODO: dictionary comprehension
new_dict = {k: v for k, v in my_dict.items()}
test_copy(my_dict,new_dict,'comprehension (shallow): ')
##✅TODO: Deep Copy
###✅TODO: deep copy with inner strings
new_dict = copy.deepcopy(my_dict)
test_copy(my_dict,new_dict,'deep copy with inner strings: ')
###✅TODO: deep copy values with inner strings
new_dict = {k: copy.deepcopy(v) for k, v in my_dict.items()}
test_copy(my_dict,new_dict,'deep copy values with inner strings:')
##✅TODO:Full copy
def full_copy(obj):
    if isinstance(obj, dict):
        return {full_copy(k): full_copy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [full_copy(x) for x in obj]
    elif isinstance(obj, tuple):
        return tuple(full_copy(x) for x in obj)
    elif isinstance(obj, set):
        return {full_copy(x) for x in obj}
    elif isinstance(obj, str):
        # создаём новый объект строки, обходя кеш
        return ''.join([c for c in obj])
    elif isinstance(obj, int):
        # создаём новый объект числа через конвертацию
        return obj + 0
    else:
        return copy.deepcopy(obj)

new_dict = full_copy(my_dict)
test_copy(my_dict,new_dict,'Full copy: ') 
'''
Mutable объекты (list, set, dict)
Immutable объекты (int, float, str, bool, None, bytes, frozenset)

| Тип копии    | Mutable объекты                                   | Immutable объекты                                                     | Безопасность                                   |
| ------------ | ------------------------------------------------- | ----------------------------------------------------------------------| ---------------------------------------------- |
| Shallow copy | Не копируются → изменения отражаются на оригинале | Совпадают или нет — не важно                                          | Опасно, если нужны независимые списки/словарь  |
| Deep copy    | Полностью копируются                              | Совпадают по id — безопасно                                           | Безопасно для mutable объектов                 |
| Full copy    | Полностью копируются, включая рекурсивно          | id может совпадать из-за кеша для маленьких чисел/строк, но безопасно | Безопасно, id для immutable обычно не критично |

'''


##✅TODO: 3. Создай список только значений найденных ключей
# решение:
values_list = [v for v in my_dict.values()]
print(values_list)

# ------------------------------
# ✅Задача 7: Конвертация типов данных из разных структур
# ------------------------------
# У нас есть данные о клиентах в виде строки CSV (`customers_string`).
# 
# Цель:
# - Научиться конвертировать данные между разными типами структур данных в Python
# - Попрактиковаться с mutable и immutable объектами, списками и словарями

customers_string = '''
id,first_name,last_name,email,gender,ip_address
1,Rania,Andrichuk,randrichuk0@sina.com.cn,Female,126.245.12.84
2,Leola,O'Carroll,locarroll1@yahoo.co.jp,Female,227.67.176.74
3,Libbi,Stanner,lstanner2@bing.com,Female,198.53.118.19
4,Tracey,Caldeiro,tcaldeiro3@loc.gov,Male,4.214.3.211
5,Marnia,Beesley,mbeesley4@google.com,Female,2.52.219.173
6,Norry,Dalzell,ndalzell5@goo.ne.jp,Female,131.35.31.168
7,Clementius,Shipway,cshipway6@baidu.com,Male,51.143.228.172
8,Diena,Dymoke,ddymoke7@nature.com,Female,132.80.141.247
9,Maribelle,Hedworth,mhedworth8@qq.com,Female,229.72.101.234
10,Lindsy,Sire,lsire9@nifty.com,Female,25.235.88.187
'''
#✅TODO: Необходимо выполнить несколько преобразований типов данных:
##✅TODO: 1. Преобразовать строку в список списков (List[List[str]]) -> List1
def convert_from_string_to_list_list_srt(string):
    result = [line.strip().split(',') for line in string.strip().split('\n')]
    return result
    
List1 = convert_from_string_to_list_list_srt(customers_string)
print(type(List1), '+', type(List1[0]))

##✅TODO: 2. Преобразовать List1 или CSV в список словарей (List[dict]) -> list2
def convert_list_to_list_dict(list_data):
    keys = list_data[0]
    values = list_data[1:]
    result = []
    for v in values:
        dicts = {}
        for i in range(len(v)):
            dicts[keys[i]] = v[i]
            
        result.append(dicts)
    
        
    return result
    
List2 = convert_list_to_list_dict(List1)
print(type(List2), '+', type(List2[0]))

##✅TODO: 3. Преобразовать строку в словарь словарей, где ключ — id клиента (dict[dict]) -> list3
def convert_string_to_dict_dict(string):
    
    keys_list = string.strip().split('\n')[0].split(',')
    values_lists = [line.strip().split(',') for line in string.strip().split('\n')[1:]]
    
    result = {}
    for v in values_lists:
        id = v[0]
        data = {keys_list[i]:v[i] for i in range(1,len(keys_list))}
        result[id] = data

    return result

List3 = convert_string_to_dict_dict(customers_string)
print(type(List3), '+' , type(List3["1"]))

##✅TODO: 4. Преобразовать List1 в словарь словарей, используя первую колонку (id) как ключ (list[list[str] to dict[dict])-> list4
def convert_list_list_to_dict_dict(list_data):
    keys_list = list_data[0]
    values = list_data[1:]
    result = {}
    for v in values:
        client_id = v[0]
        result[client_id] = {keys_list[i]:v[i] for i in range(1, len(keys_list))}
    return result

List4 = convert_list_list_to_dict_dict(List1)
print(type(List4), '+' , type(List4["1"]))


# Дополнительно:
# - Использовать циклы и конструкторы (dict(), list(), и т.д.)
# - Использовать встроенные функции:
#     - enumerate()
#     - zip()
#     - sorted() для сортировки по нужным полям

# ------------------------------
##✅TODO: 1️⃣ CSV -> List[List[str]]
def convert_from_string_to_list_list_csv(file_data):
    return [line.strip().split(',') for line in file_data.strip().split('\n')]

List1 = convert_from_string_to_list_list_csv(customers_string)


# ------------------------------
##✅TODO: 2️⃣ List[List[str]] -> List[dict]
def convert_list_to_list_dict(list_data):
    keys = list_data[0]
    return [{k: v for k, v in zip(keys, row)} for row in list_data[1:]]

List2 = convert_list_to_list_dict(List1)


# ------------------------------
##✅TODO: 3️⃣ CSV -> dict[dict] с внешним ключом id
def convert_string_to_dict_dict_csv(file_data):
    lines = file_data.strip().split('\n')
    keys = lines[0].split(',')
    result = {
        row.split(',')[0]: {k: v for k, v in zip(keys[1:], row.split(',')[1:])} 
        for row in lines[1:]
    }
    return result

List3 = convert_string_to_dict_dict_csv(customers_string)


# ------------------------------
##✅TODO: 4️⃣ List[List[str]] -> dict[dict] с внешним ключом id
def convert_list_list_to_dict_dict(list_data):
    keys = list_data[0]
    return {
        row[0]: {k: v for k, v in zip(keys[1:], row[1:])} 
        for row in list_data[1:]
    }

List4 = convert_list_list_to_dict_dict(List1)


# ------------------------------
# Дополнительно: сортировка по last_name
List4_sorted = dict(sorted(List4.items(), key=lambda item: item[1]['last_name']))

# Выводим для проверки
print("List1:", type(List1), '+', type(List1[0]))
print("List2:", type(List2), '+', type(List2[0]))
print("List3:", type(List3), '+', type(List3["1"]))
print("List4:", type(List4), '+', type(List4["1"]))
print("List4_sorted:", List4_sorted)

# ------------------------------
##✅TODO: 2️⃣ List[List[str]] -> List[dict] (через enumerate)
def convert_list_to_list_dict_enum(list_data):
    keys = list_data[0]
    result = []
    for row in list_data[1:]:
        d = {keys[i]: val for i, val in enumerate(row)}
        result.append(d)
    return result

List2_enum = convert_list_to_list_dict_enum(List1)


# ------------------------------
##✅TODO: 3️⃣ CSV -> dict[dict] с внешним ключом id (через enumerate)
def convert_string_to_dict_dict_enum(string):
    lines = string.strip().split('\n')
    keys = lines[0].split(',')
    result = {}
    for row in lines[1:]:
        values = row.split(',')
        client_id = values[0]
        # начиная с индекса 1, т.к. id выносим отдельно
        data = {keys[i]: val for i, val in enumerate(values) if i != 0}
        result[client_id] = data
    return result

List3_enum = convert_string_to_dict_dict_enum(customers_string)


# ------------------------------
##✅TODO: 4️⃣ List[List[str]] -> dict[dict] (через enumerate)
def convert_list_list_to_dict_dict_enum(list_data):
    keys = list_data[0]
    result = {}
    for row in list_data[1:]:
        client_id = row[0]
        data = {keys[i]: val for i, val in enumerate(row) if i != 0}
        result[client_id] = data
    return result

List4_enum = convert_list_list_to_dict_dict_enum(List1)

# Проверка
print("List2_enum[0]:", List2_enum[0])
print("List3_enum['1']:", List3_enum['1'])
print("List4_enum['1']:", List4_enum['1'])



# ------------------------------
#✅TODO: Дополнительные задания для практики с преобразованием данных
# ------------------------------
print ('-'*100)
#✅TODO: 5. Преобразовать данные в множество кортежей (Set[Tuple[str]]), чтобы оставить только уникальные записи.
def convert_list_to_set_tuple(list_data):
    result = set()
    for v in list_data[1:]:
        tpl = tuple(v)
        result.add(tpl)
    
    return result

List6 = convert_list_to_set_tuple(List1)
print(type(List6), '\n', List6)

print ('-'*100)

def convert_list_to_set_tuple(list_data: list) -> set[tuple]:
    """Преобразует список в множество кортежей для удаления дубликатов."""
    return {tuple(item) for item in list_data} if list_data else set()

#✅TODO: Или еще короче:
def convert_list_to_set_tuple(list_data: list) -> set[tuple]:
    return set(tuple(item) for item in list_data)

#✅TODO: 6. Превратить данные в словарь, где ключ — какое-либо поле (например, 'gender'), а значение — список всех клиентов с этим значением (dict[str, List[List[str]]]).
def convert_data_to_dict(data) -> dict:
    if isinstance(data, str):
        print('data in string format')
        list_data = [line.strip().split(',') for line in data.strip().split('\n')]
        pass
    elif isinstance(data, list):
        print('data in list format')
        list_data = data
        pass
    else: print('unsopported data format')
    
    keys = list_data[0]
    gender_index = -1
    values_list = list_data[1:]
    print(values_list)
    for i, key in enumerate(keys):
        if key.strip().lower() == 'gender':  # Более гибкое сравнение
            gender_index = i
            break
        
    print(gender_index) 
    
    dictionary = {}
    for row in values_list:
        if gender_index < len(row):  # Проверяем, что в строке есть gender
            gender_value = row[gender_index].strip()
            
            # Если такого gender еще нет в словаре, создаем пустой список
            if gender_value not in dictionary:
                dictionary[gender_value] = []
            
            # Добавляем всю строку в список для данного gender
            dictionary[gender_value].append(row)
            
            #dictionary.setdefault(gender_value, []).append(row)  # 1 строка вместо 3
        
    return dictionary

print(convert_data_to_dict(customers_string))
print(convert_data_to_dict(List1))
        
#✅TODO: 7. Сгруппировать данные по выбранному ключу (например, первая буква фамилии) в словарь списков (dict[str, List[List[str]]]).
def group_by_lastname_firstletter(list1):
    dictionary = {}
    last_name_index = -1
    for i, k in enumerate(list1[0]):
        if k.strip().lower() == 'last_name':
            last_name_index = i
            break
            
    for row in list1[1:]:
        if last_name_index < len(row):
            last_name_value = row[last_name_index].strip()
            dictionary.setdefault(last_name_value[0].upper(), []).append(last_name_value)
        
    print(dictionary)
    
group_by_lastname_firstletter(List1)
#TODO: преобразование типов данных
##TODO: 8. Преобразовать данные в список NamedTuple для каждого клиента.

##TODO: 9. Использовать dataclass для описания структуры клиента и создать список экземпляров.
##TODO: 10. Преобразовать данные в Pandas DataFrame и выполнить сортировку, фильтрацию и группировку.
##TODO: 11. Сериализовать словарь или список словарей в JSON для хранения или передачи.

##TODO: 12. Попробовать объединить несколько структур: например, dict[tuple] или dict[set] для определённых полей.
##TODO: 13. Практика с встроенными функциями: enumerate(), zip(), sorted(), map(), filter() для различных представлений данных.


