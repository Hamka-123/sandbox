#Strings - Строки
'''
string1 = "Text"
string2 = 'Text'

Метод	Описание на русском
capitalize()	Делает первую букву строки заглавной, остальные — строчными.
casefold()	Преобразует строку в нижний регистр (более агрессивно, чем lower()).
center()	Центрирует строку в заданной ширине, дополняя пробелами.
count()	Считает, сколько раз заданное значение встречается в строке.
encode()	Кодирует строку в байты (например, в UTF-8).
endswith()	Проверяет, заканчивается ли строка заданным значением.
expandtabs()	Заменяет символы табуляции на пробелы с указанным размером таба.
find()	Ищет заданное значение и возвращает индекс первого вхождения или -1.
format()	Форматирует строку, подставляя значения по шаблону.
format_map()	Аналог format(), работает с отображениями (dict).
index()	Ищет заданное значение и возвращает индекс первого вхождения. Ошибка, если не найдено.
isalnum()	Проверяет, состоит ли строка только из букв и цифр.
isalpha()	Проверяет, состоит ли строка только из букв.
isascii()	Проверяет, состоит ли строка из ASCII-символов (код 0–127).
isdecimal()	Проверяет, состоит ли строка из десятичных цифр.
isdigit()	Проверяет, состоит ли строка из цифр (включая надстрочные и т.п.).
isidentifier()	Проверяет, может ли строка быть идентификатором (именем переменной).
islower()	Проверяет, что все буквы в строке — строчные.
isnumeric()	Проверяет, состоит ли строка из числовых символов.
isprintable()	Проверяет, что все символы строки — печатаемые.
isspace()	Проверяет, что строка состоит только из пробельных символов.
istitle()	Проверяет, что строка оформлена в формате заголовка (каждое слово с заглавной буквы).
isupper()	Проверяет, что все буквы в строке — заглавные.
join()	Объединяет последовательность строк, вставляя между ними данный разделитель.
ljust()	Выравнивает строку по левому краю, дополняя справа пробелами.
lower()	Преобразует строку в нижний регистр.
lstrip()	Удаляет пробелы (или указанные символы) слева.
maketrans()	Создаёт таблицу перевода символов для метода translate().
partition()	Делит строку на три части по первому вхождению разделителя: (до, разделитель, после).
replace()	Заменяет в строке указанное значение на другое.
rfind()	Ищет последнее вхождение значения и возвращает индекс или -1.
rindex()	Ищет последнее вхождение значения и возвращает индекс, ошибка если не найдено.
rjust()	Выравнивает строку по правому краю, дополняя слева пробелами.
rpartition()	Делит строку на три части по последнему вхождению разделителя.
rsplit()	Разбивает строку справа по разделителю, возвращает список.
rstrip()	Удаляет пробелы (или указанные символы) справа.
split()	Разбивает строку по разделителю, возвращает список.
splitlines()	Разбивает строку на список по переносам строк.
startswith()	Проверяет, начинается ли строка с заданного значения.
strip()	Удаляет пробелы (или указанные символы) с обеих сторон.
swapcase()	Меняет регистр букв на противоположный (верхний → нижний и наоборот).
title()	Делает первую букву каждого слова заглавной.
translate()	Заменяет символы в строке по таблице перевода.
upper()	Преобразует строку в верхний регистр.
zfill()	Добавляет в начало строки нули до заданной длины.
'''
#попробовать каждый метод
'''
test_string1 = "test"

print(test_string1.capitalize())  # 'Test'
print(test_string1.casefold())  # 'test'
print(test_string1.center(10))  # '   test   '
print(test_string1.count('t'))  # 2
print(test_string1.encode('utf-8')) #b'test'

test_string2 = "t\te\ts\tt"
print(test_string2) # 't   e   s   t'
print(test_string1.expandtabs(0))  # 'test'

print(test_string1.find('e'))  # 1
print(test_string1.find('x'))  # -1
print(test_string1.find('t'))  # 0

test_string3 = "test{variable}"
print(test_string3.format(variable='ing'))  # 'testing'
print(test_string3.format_map({'variable': 'ing'}))  # 'testing'

print(test_string1.index('e'))  # 1
#print(test_string1.index('x'))  # ValueError
print(test_string1.index('t'))  # 0

print(test_string1.isalnum())  # True
print(test_string1.isalpha())  # True
print(test_string1.isascii())  # True
print(test_string1.isdecimal())  # False
print(test_string1.isdigit())  # False
print(test_string1.isidentifier())  # True
test_string4 = "3423asfsf"
print(test_string4.isidentifier())  # False
print(test_string1.islower())  # True
print(test_string1.isnumeric())  # False
print(test_string1.isprintable())  # True
test_string5 = "test\n"
print(test_string5.isprintable())  # False
print(test_string1.isspace())  # False
print(test_string1.istitle())  # False
test_string6 = "Test String"
print(test_string6.istitle())  # True
print(test_string1.isupper())  # False

print(test_string1.join(['a', 'b', 'c']))  # 'atestbtestc'
print(test_string1.ljust(10))  # 'test      '
print(test_string1.rjust(10))  # '      test'
print(test_string1.lower())  # 'test'
print(test_string1.upper())  # 'TEST'
print(test_string1.swapcase())  # 'TEST'

test_string7 = '   test   '
print(test_string7.lstrip())  # 'test   '
print(test_string7.rstrip())  # '   test'
print(test_string7.strip())  # 'test'

print(test_string1.maketrans('t', 'T'))  # {116: 84}
print(test_string1.translate(str.maketrans('t', 'T')))  # 'TesT'
print(test_string1.partition('e'))  # ('t', 'e', 'st')
print(test_string1.replace('t', 'T'))  # 'Test'
print(test_string1.rfind('t'))  # 3
print(test_string1.rindex('t'))  # 3
print(test_string1.rpartition('e'))  # ('tes', 'e', 't')

print(test_string1.split('e'))  # ['t', 'st']
print(test_string1.rsplit('t'))  # ['', 'es', '']
print(test_string1.splitlines())  # ['test']
print(test_string1.startswith('t'))  # True

print(test_string1.endswith('e'))  #False
print(test_string1.title())  # 'Test'
print(test_string1.zfill(10))  # '000000test'

'''
tables = [
    "users",
    "emails"
         ]
names = [
    "avi",
    "admin@corp.com"
         ]
SQL_TEMPLATE = "SELECT * FROM {table} WITH name = {name}" 
sql_query_1 = SQL_TEMPLATE.format(name=names[0], table=tables[0]) # ✅
sql_query_2 = SQL_TEMPLATE.format(names[1], tables[1]) # ❌
print(sql_query_1)
print(sql_query_2)

