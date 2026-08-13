
import pathlib
import json


DATA_FOLDER_ROOT = pathlib.Path(__file__).parent.joinpath("datafiles")
SOURCE_FILE = DATA_FOLDER_ROOT.joinpath("rates_1.json")

#read json
#print ILS rate

with open(SOURCE_FILE, 'r') as f:
    data = json.load(f)
    pass

print(data["rates"]["ILS"])

# currency converter
data_currencies = data['rates'].keys()
default_from = "AFN"
default_to = "AED"
default_sum = 100

print(f'''
Валюты, какие можем менять:
{", ".join(data_currencies)}\n
      ''')

currencies_from_convert = input(f"Какую валюту будем менять? [default: {default_from}]") or default_from
currencies_to_convert = input(f"На какую валюту будем менять? [default: {default_to}]") or default_to
sum_to_convert = input(f"Сколько хотим поменять? [default: {default_sum}] ") or default_sum


sum_after_convert = int(sum_to_convert) * (data["rates"][currencies_to_convert] / data["rates"][currencies_from_convert])

print(f"Возьмите свои {sum_after_convert:.2f} {currencies_to_convert}")


#-------------------------
print('---------------------------------------------')
#chat gpt refactoring:
'''
✅ Что улучшено:
Безопасный ввод числа (int) с обработкой ошибок.
Проверяется, что валюта есть в списке data['rates']
Если пользователь вводит пустую строку — используется значение по умолчанию.
Функции для повторного использования: input_with_default и input_int_with_default.
Красивый вывод валют по 10 в строке.
Код стал читаемым и структурированным.
'''
#-------------------------
# currency converter с проверкой валют

def input_with_default(prompt, default, valid_options=None):
    """
    Безопасный ввод с дефолтным значением.
    valid_options — список допустимых значений (необязательно).
    """
    while True:
        user_input = input(f"{prompt} [default: {default}] ").strip()
        value = user_input if user_input else default
        if valid_options and value not in valid_options:
            print(f"Некорректная валюта. Допустимые варианты: {', '.join(valid_options[:10])} ...")
            continue
        return value

def input_int_with_default(prompt, default):
    """Безопасный ввод числа с дефолтом"""
    while True:
        user_input = input(f"{prompt} [default: {default}] ").strip()
        if not user_input:
            return default
        try:
            return int(user_input)
        except ValueError:
            print(f"Введено не число. Попробуйте снова.")

# Настройки
data_currencies = list(data['rates'].keys())
default_from = "AFN"
default_to = "AED"
default_sum = 100

# Выводим валюты красиво по 10 в строке
print("Валюты, какие можем менять:")
for i in range(0, len(data_currencies), 10):
    print(", ".join(data_currencies[i:i+10]))
print()

# Ввод данных с проверкой
currencies_from = input_with_default("Какую валюту будем менять?", default_from, data_currencies)
currencies_to = input_with_default("На какую валюту будем менять?", default_to, data_currencies)
sum_to_convert = input_int_with_default("Сколько хотим поменять?", default_sum)

# Конвертация
sum_after_convert = sum_to_convert * (data["rates"][currencies_to] / data["rates"][currencies_from])

# Вывод результата
print(f"Возьмите свои {sum_after_convert:.2f} {currencies_to}")
