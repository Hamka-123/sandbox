"""
🦄 ШПАРГАЛКА ПО REGEX (регулярным выражениям)
Основные концепции и примеры для Python
"""

import re

# ==================== ОСНОВНЫЕ СИМВОЛЫ ====================

# 🔹 БАЗОВЫЕ СИМВОЛЫ
pattern = r"abc"           # Точное совпадение "abc"
pattern = r"a.c"           # Любой символ между a и c: "abc", "a c", "a-c"
pattern = r"a\.c"          # Точка как символ: "a.c" (экранирование)

# 🔹 СПЕЦИАЛЬНЫЕ СИМВОЛЫ
pattern = r"\d"            # Любая цифра: "0", "1", ..., "9"
pattern = r"\D"            # НЕ цифра: буквы, символы
pattern = r"\w"            # Буквенно-цифровой символ + нижнее подчеркивание: "a", "Z", "0", "_"
pattern = r"\W"            # НЕ буквенно-цифровой: пробелы, знаки препинания
pattern = r"\s"            # Пробельный символ: пробел, табуляция, новая строка
pattern = r"\S"            # НЕ пробельный символ

# 🔹 КВАНТИФИКАТОРЫ (количество повторений)
pattern = r"a*"            # 0 или более раз: "", "a", "aa", "aaa", ...
pattern = r"a+"            # 1 или более раз: "a", "aa", "aaa", ...
pattern = r"a?"            # 0 или 1 раз: "", "a"
pattern = r"a{3}"          # Ровно 3 раза: "aaa"
pattern = r"a{2,4}"        # От 2 до 4 раз: "aa", "aaa", "aaaa"
pattern = r"a{2,}"         # 2 или более раз: "aa", "aaa", ...

# ==================== ГРУППЫ И КЛАССЫ ====================

# 🔹 КЛАССЫ СИМВОЛОВ
pattern = r"[abc]"         # Любой из символов: "a", "b", "c"
pattern = r"[a-z]"         # Любая строчная буква
pattern = r"[A-Z]"         # Любая заглавная буква
pattern = r"[0-9]"         # Любая цифра
pattern = r"[a-zA-Z]"      # Любая буква
pattern = r"[^abc]"        # НИ ОДИН из символов: не "a", не "b", не "c"

# 🔹 ГРУППИРОВКА
pattern = r"(abc)+"        # Группа: "abc", "abcabc", ...
pattern = r"(a|b)"         # ИЛИ: "a" или "b"
pattern = r"(?P<name>...)" # Именованная группа

# ==================== ЯКОРЯ И ГРАНИЦЫ ====================

# 🔹 ЯКОРЯ (позиции в тексте)
pattern = r"^abc"          # Начало строки: "abc..." 
pattern = r"abc$"          # Конец строки: "...abc"
pattern = r"\bword\b"      # Граница слова: "word", но не "keyword"
pattern = r"\Bword\B"      # НЕ граница слова: "keyword", но не "word"

# ==================== ПРАКТИЧЕСКИЕ ПРИМЕРЫ ====================

# 🔹 EMAIL
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
# Пример: "user@example.com", "test.email+tag@domain.co.uk"

# 🔹 ТЕЛЕФОН (российский)
phone_pattern = r"^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$"
# Пример: "+7-912-345-67-89", "8(912)3456789", "89123456789"

# 🔹 URL
url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*\??[/\w\.-=&%]*"
# Пример: "http://example.com", "https://site.com/path?param=value"

# 🔹 IP АДРЕС
ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
# Пример: "192.168.1.1", "127.0.0.1"

# 🔹 ДАТА (dd.mm.yyyy)
date_pattern = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$"
# Пример: "31.12.2023", "01.01.2024"

# ==================== ФЛАГИ (МОДИФИКАТОРЫ) ====================

# re.IGNORECASE или re.I - игнорировать регистр
result = re.findall(r"python", "Python PYTHON python", re.IGNORECASE)

# re.MULTILINE или re.M - многострочный режим
result = re.findall(r"^abc", "abc\nabc", re.MULTILINE)

# re.DOTALL или re.S - точка включает перевод строки
result = re.findall(r"a.b", "a\nb", re.DOTALL)

# re.VERBOSE или re.X - игнорировать пробелы и комментарии
pattern = re.compile(r"""
    \d{3}           # три цифры
    -               # дефис
    \d{2}           # две цифры
    -               # дефис  
    \d{2}           # две цифры
""", re.VERBOSE)

# ==================== МЕТОДЫ РАБОТЫ С REGEX ====================

text = "Мой email: test@example.com и телефон: +7-912-345-67-89"

# 🔹 ПОИСК (первое совпадение)
match = re.search(r"\b\w+@\w+\.\w+\b", text)
if match:
    print(f"Найден email: {match.group()}")  # test@example.com

# 🔹 ПОИСК ВСЕХ СОВПАДЕНИЙ
emails = re.findall(r"\b\w+@\w+\.\w+\b", text)
print(f"Все email: {emails}")  # ['test@example.com']

# 🔹 РАЗБИТЬ СТРОКУ
parts = re.split(r"\s*[:]\s*", text)  # Разделить по двоеточию с пробелами
print(f"Разделенная строка: {parts}")

# 🔹 ЗАМЕНА
new_text = re.sub(r"\+\d-\d{3}-\d{3}-\d{2}-\d{2}", "[ТЕЛЕФОН]", text)
print(f"После замены: {new_text}")

# 🔹 КОМПИЛЯЦИЯ ПАТТЕРНА (для многократного использования)
phone_regex = re.compile(r"\+\d-\d{3}-\d{3}-\d{2}-\d{2}")
matches = phone_regex.findall(text)

'''
re.finditer()
re.match()
re.escape()
re.fullmatch()
re.subn()
'''

# ==================== ГРУППЫ И ИХ ИСПОЛЬЗОВАНИЕ ====================

text = "Иван: 30 лет, Мария: 25 лет"

# 🔹 ИЗВЛЕЧЕНИЕ ГРУПП
matches = re.findall(r"(\w+):\s*(\d+)\s*лет", text)
for name, age in matches:
    print(f"Имя: {name}, Возраст: {age}")
# Вывод: Имя: Иван, Возраст: 30
#        Имя: Мария, Возраст: 25

# 🔹 ИМЕНОВАННЫЕ ГРУППЫ
pattern = r"(?P<name>\w+):\s*(?P<age>\d+)\s*лет"
match = re.search(pattern, text)
if match:
    print(f"Имя: {match.group('name')}")  # Иван
    print(f"Возраст: {match.group('age')}")  # 30

# 🔹 ЖАДНЫЕ vs ЛЕНИВЫЕ КВАНТИФИКАТОРЫ
text = "<div>content</div>"

# ЖАДНЫЙ (greedy) - берет максимально возможное
greedy = re.findall(r"<.*>", text)  # ['<div>content</div>']

# ЛЕНИВЫЙ (lazy) - берет минимально возможное  
lazy = re.findall(r"<.*?>", text)   # ['<div>', '</div>']

# ==================== ПОЛЕЗНЫЕ ШАБЛОНЫ ====================

# 🔹 ПАРОЛЬ (минимум 8 символов, буквы и цифры)
password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

# 🔹 HEX ЦВЕТ (#FFFFFF)
color_pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"

# 🔹 ВРЕМЯ (HH:MM)
time_pattern = r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$"

# 🔹 ИМЯ ФАЙЛА С РАСШИРЕНИЕМ
filename_pattern = r"^[\w\s\-]+\.[a-zA-Z]{2,4}$"

# 🔹 УДАЛЕНИЕ HTML ТЕГОВ
clean_text = re.sub(r"<[^>]+>", "", "<div>Hello</div>")  # "Hello"

# ==================== ОТЛАДКА И ТЕСТИРОВАНИЕ ====================

def test_regex(pattern, test_cases):
    """Функция для тестирования regex паттернов"""
    compiled = re.compile(pattern)
    print(f"Тестируем паттерн: {pattern}")
    print("-" * 50)
    
    for test in test_cases:
        result = "✅" if compiled.match(test) else "❌"
        print(f"{result} '{test}'")
    
    print()

# Пример тестирования
test_cases = ["abc", "abcd", "ab", "ac", "a c"]
test_regex(r"a.c", test_cases)

"""
💡 СОВЕТЫ:
1. Используйте r"..." для raw strings (избегайте двойного экранирования)
2. Тестируйте на https://regex101.com/ или https://regexr.com/
3. Начинайте с простых паттернов, постепенно усложняйте
4. Используйте группы для извлечения данных
5. Помните о жадных и ленивых квантификаторах
"""