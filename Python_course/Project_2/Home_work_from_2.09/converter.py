# every task -> single function !!!!

# get rates online
## requests
# get rates from file (JSON)

# save conversions history (SCV file)
##  file.write()  print(file = )

#  get file data -> rates
# pip install requests

# ------------------------------------------------------------------------------------------------
# -- imports
# ------------------------------------------------------------------------------------------------
import json
import pathlib
import requests
import csv

# ------------------------------------------------------------------------------------------------
# -- configuration
# ------------------------------------------------------------------------------------------------
EXCHANGERATE_URL = 'https://api.exchangerate-api.com/v4/latest/USD'

ROOT_FOLDER = pathlib.Path(__file__).parent
JSON_RATES_FOLDER = ROOT_FOLDER.joinpath("rates_data")
LOG_FOLDER = ROOT_FOLDER.joinpath("conversions_history")
LOG_FILE = LOG_FOLDER.joinpath("history.csv")
SOURCE_FILE_1 = JSON_RATES_FOLDER.joinpath("rates.json")
# ------------------------------------------------------------------------------------------------
# -- functions
# ------------------------------------------------------------------------------------------------
def get_online_data(URL):
    """
    Получает данные о курсах валют онлайн.

    Args:
        URL (str): Ссылка на API с курсами валют.

    Returns:
        tuple: (rates, date)
            rates (dict or None): Словарь курсов валют, где ключ — код валюты.
            date (str or None): Дата курсов.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()  # выбросит ошибку, если статус != 200
        data_json = response.json()
        rates = data_json.get("rates")
        date = data_json.get("date")
        return rates, date
    except Exception as e:
        print(f"Не удалось получить онлайн-данные: {e}")
        return None, None

def get_data_from_file(file):
    """
    Читает данные о курсах валют из локального JSON-файла.

    Args:
        file (str or pathlib.Path): Путь к JSON-файлу.

    Returns:
        tuple: (rates, date)
            rates (dict): Словарь курсов валют.
            date (str): Дата курсов.
    """
    with open(file) as f:
        data_json = json.load(f)
        return data_json.get("rates"), data_json.get("date")

def get_rates():
    """
    Получает курсы валют: сначала онлайн, если не получилось — из локального файла.

    Returns:
        tuple: (rates, date)
            rates (dict): Словарь курсов валют.
            date (str): Дата курсов.
    """
    rates, date = get_online_data(EXCHANGERATE_URL)
    if rates:
        print(f"Данные взяты онлайн на дату: {date}")
        return rates, date
    else:
        rates, date = get_data_from_file(SOURCE_FILE_1)
        print(f"Используем локальные данные на дату: {date}")
        return rates, date

def input_with_default(prompt, default, valid_options=None):
    """
    Запрашивает строковый ввод пользователя с дефолтным значением.
    Проверяет, что ввод содержится в valid_options (если передан список допустимых значений).
    Возвращает безопасное значение (в верхнем регистре).

    Args:
        prompt (str): Сообщение для пользователя.
        default (str): Значение по умолчанию, если пользователь не ввёл ничего.
        valid_options (list of str, optional): Список допустимых значений. Defaults to None.

    Returns:
        str: Введённое пользователем значение или default (в верхнем регистре).
    """
    valid_options_upper = [v.upper() for v in valid_options] if valid_options else None
    while True:
        user_input = input(f"{prompt} [default: {default}] ").strip().upper()
        value = user_input if user_input else default.upper()
        if valid_options_upper and value not in valid_options_upper:
            print(f"Некорректная валюта. Допустимые варианты: {', '.join(valid_options[:10])} ...")
            continue
        return value

def input_int_with_default(prompt, default):
    """
    Запрашивает числовой ввод пользователя с дефолтным значением.
    Если пользователь не ввёл значение — возвращается default.
    Повторяет запрос, пока не будет введено корректное число.

    Args:
        prompt (str): Сообщение для пользователя.
        default (int): Значение по умолчанию.

    Returns:
        int: Введённое пользователем число или default.
    """
    """Безопасный ввод числа с дефолтом"""
    while True:
        user_input = input(f"{prompt} [default: {default}] ").strip()
        if not user_input:
            return default
        try:
            return int(user_input)
        except ValueError:
            print(f"Введено не число. Попробуйте снова.")
            
def prettify_print_currencies(currencies):
    """
    Красиво выводит список валют по 10 штук в строке.

    Args:
        currencies (list of str): Список кодов валют.
    """
    print("Валюты, какие можем менять:")
    for i in range(0, len(currencies), 10):
        print(", ".join(currencies[i:i+10]))
    print()
    
def get_user_data(default_from, default_to, default_sum, data):
    """
    Запрашивает у пользователя исходную валюту, валюту для конверсии и сумму для обмена.

    Args:
        default_from (str): Валюта по умолчанию для обмена.
        default_to (str): Валюта по умолчанию для получения.
        default_sum (int): Сумма по умолчанию.
        data (dict): Словарь доступных валют.

    Returns:
        tuple: (currencies_from, currencies_to, sum_to_convert)
            currencies_from (str): Валюта для обмена.
            currencies_to (str): Валюта для получения.
            sum_to_convert (int): Сумма для обмена.
    """
    currencies_from = input_with_default("Какую валюту будем менять?", default_from, data)
    currencies_to = input_with_default("На какую валюту будем менять?", default_to, data)
    sum_to_convert = input_int_with_default("Сколько хотим поменять?", default_sum)
    return currencies_from, currencies_to, sum_to_convert

def converter(currencies_from, currencies_to, sum_to_convert, data):
    """
    Конвертирует сумму из одной валюты в другую.

    Args:
        currencies_from (str): Валюта для обмена.
        currencies_to (str): Валюта для получения.
        sum_to_convert (int or float): Сумма для обмена.
        data (dict): Словарь курсов валют.

    Returns:
        float: Сумма после конверсии.
    """
    return sum_to_convert * (data[currencies_to] / data[currencies_from])

def convert_and_print(currencies_from, currencies_to, sum_to_convert, data):
    """
    Конвертирует и выводит результат пользователю.

    Args:
        currencies_from (str): Валюта для обмена.
        currencies_to (str): Валюта для получения.
        sum_to_convert (int or float): Сумма для обмена.
        data (dict): Словарь курсов валют.

    Returns:
        float: Сумма после конверсии.
    """
    sum_after_convert = converter(currencies_from, currencies_to, sum_to_convert, data)
    print(f"Возьмите свои {sum_after_convert:.2f} {currencies_to}")
    return sum_after_convert

def save_history_csv(date, sum_from, currency_from, sum_to, currency_to):
    """
    Сохраняет историю конверсий в CSV-файл с заголовками.

    Args:
        date (str): Дата курсов валют.
        sum_from (float): Сумма исходной валюты.
        currency_from (str): Исходная валюта.
        sum_to (float): Конвертированная сумма.
        currency_to (str): Валюта после конверсии.
    """
    # Создаём папку, если её нет
    LOG_FOLDER.mkdir(exist_ok=True)
    
    # Проверяем, есть ли файл, чтобы добавить заголовки
    file_exists = LOG_FILE.exists()
    file_empty = True
    if file_exists:
        file_empty = LOG_FILE.stat().st_size == 0  # проверяем размер файла
    
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        
        # Записываем заголовок только если файл новый
        if not file_exists or file_empty:
            writer.writerow(["date", "sum_from", "currency_from", "sum_to", "currency_to"])
        
        # Записываем строку конверсии
        writer.writerow([date, f"{sum_from:.2f}", currency_from, f"{sum_to:.2f}", currency_to])

            
# ------------------------------------------------------------------------------------------------
# -- main
# ------------------------------------------------------------------------------------------------
# Получаем курсы валют
data, date = get_rates()
currencies = list(data.keys())
# значения по умолчанию для пользовательских данных
default_from = "AFN"
default_to = "AED"
default_sum = 100

while True:
    choice = input("Convert? [y] / Exit [any key]: ").strip().upper()
    if not choice.startswith("Y"):
        print("Выход из конвертера.")
        break
    prettify_print_currencies(currencies)
    currencies_from, currencies_to, sum_to_convert = get_user_data(
        default_from, default_to, default_sum, data
    )
    sum_after_convert = convert_and_print(
        currencies_from, currencies_to, sum_to_convert, data
    )
    save_history_csv(date, sum_to_convert, currencies_from, sum_after_convert, currencies_to)
