from pathlib import Path
import sqlite3
import config
from mybudget import constants
from .constants import *


#init
def init():
    create_working_dirs(config.ROOT_FOLDER)
    conn = create_db(config.DB_PATH)
    create_tables(conn)
    return conn
  

def create_working_dirs(root_folder: str):
    """
    Создаёт все рабочие папки проекта, если они ещё не существуют.
    """
    # список папок, которые нужны проекту
    dirs = [
        Path(root_folder),
        Path(config.DB_PATH),      # папка для базы данных
        Path(config.REPORT_PATH),         # папка для отчётов 
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def create_db(DB_PATH):
    """Создаёт базу данных и подключается к ней"""
    DB = DB_PATH.joinpath(DB_NAME)
    return sqlite3.connect(DB)

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(constants.SQL_CREATE_TABLE_CATEGORIES)
    cursor.execute(constants.SQL_CREATE_TABLE_TRANSACTIONS)

#main
def display_main_menu(): return MAIN_MENU

#crud
def create_transaction(conn, category_name, date, transactions_amount, current_balance, comments):
    cursor = conn.cursor()
    category_id = get_category_id(conn, category_name)
    if not category_id:
        category_id = create_category(conn, category_name)
    cursor.execute(constants.SQL_INSERT_TRANSACTION, (category_id, date, transactions_amount, current_balance, comments,))
    conn.commit()

def get_category_id(conn, category_name):
    cursor = conn.cursor()
    cursor.execute(constants.SQL_SELECT_CATEGORY, (category_name,))
    result = cursor.fetchone()
    if result:
        return result[0]  # возвращаем сам id
    return None

def create_category(conn, category_name):
    cursor = conn.cursor()
    category_id = get_category_id(conn, category_name)
    if category_id is None:
        cursor.execute(constants.SQL_INSERT_CATEGORY, (category_name,))
        conn.commit()
        return cursor.lastrowid
    return category_id
    
def get_categories(conn):
    cursor = conn.cursor()
    cursor.execute(constants.SQL_GET_CATEGORIES)
    rows = cursor.fetchall()
    return [row[0] for row in rows]
     
def calculate_balance(conn, transactions_amount):
    last_balance = get_current_balance(conn)
    current_balance = last_balance + transactions_amount
    return current_balance

def get_current_balance(conn):
    cursor = conn.cursor()
    cursor.execute(constants.SQL_GET_LAST_BALANCE)
    row = cursor.fetchone()
    return row[0] if row else 0

def get_transactions_per_period(conn, start_date, end_date):
    cursor = conn.cursor()
    cursor.execute(constants.GET_TRANSACTIONS_PER_PERIOD, (start_date, end_date,))
    rows = cursor.fetchall()
    return rows

def get_inc_exp_data(conn, start_date, end_date):
    data = get_transactions_per_period(conn, start_date, end_date)
    incomes = []
    expenses = []
    for trans in data:
        if trans[3] < 0:
            expenses.append(trans)
        elif trans[3] > 0: 
            incomes.append(trans)

    return incomes, expenses

def convert_tuple_to_dict(report_tuple):
    # Создаем список словарей
    data_dicts = []
    for line in report_tuple:
        dict = {
            'id': line[0],
            'user_id': line[1],
            'date': line[2],
            'amount': line[3],
            'balance': line[4],
            'description': line[5],
            'category_id': line[6],
            'category_name': line[7]
        }
        data_dicts.append(dict)
    return data_dicts

def get_transactions_per_category(transactions):
    """
    Суммирует транзакции по категориям
    transactions: список кортежей из БД - передавать отдельно доходы и расходы
    """
    transactions_dicts = convert_tuple_to_dict(transactions)

    transactions_by_category = {}
    for transaction in transactions_dicts:
        category = transaction['category_name']
        amount = abs(transaction['amount'])
        
        if category in transactions_by_category:
            transactions_by_category[category] += amount
        else:
            transactions_by_category[category] = amount
    
    return transactions_by_category, transactions_dicts

def prepare_data_to_report(conn, start_date, end_date):
    # Получаем данные
    incomes, expenses = get_inc_exp_data(conn, start_date, end_date)
    total_income = sum(trans[3] for trans in incomes if trans[3] > 0)
    total_expense = sum(abs(trans[3]) for trans in expenses if trans[3] < 0)
    balance = total_income - total_expense
    currency = '₪'
    res = {
        "incomes": incomes,
        "expenses": expenses,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "currency": currency
    }
    return res
        
def generate_report_simple_template(conn, start_date, end_date, output_file=None, template_file="simple_report.html"):
    """
    Простая загрузка шаблона из файла
    """
    data = prepare_data_to_report(conn, start_date, end_date)
    
    # Читаем шаблон из файла
    template_path = Path(__file__).parent / "report_templates" / template_file
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Простая замена (без Jinja2)
    html_content = template_content
    html_content = html_content.replace('{{ start_date }}', start_date)
    html_content = html_content.replace('{{ end_date }}', end_date)
    html_content = html_content.replace('{{ total_income }}', f'{data['total_income']:,.2f}')
    html_content = html_content.replace('{{ total_expense }}', f'{data['total_expense']:,.2f}')
    html_content = html_content.replace('{{ balance }}', f'{data['balance']:,.2f}')
    html_content = html_content.replace('{{ currency }}', data['currency'])
   
    
    # Генерируем таблицы
    incomes_html = ''.join(
        f'<tr><td>{t[2][:10]}</td><td class="positive">+{t[3]:.2f} {data['currency']}</td>'
        f'<td>{t[7]}</td><td>{t[5]}</td></tr>'
        for t in data['incomes'] if t[3] > 0
    )
    
    expenses_html = ''.join(
        f'<tr><td>{t[2][:10]}</td><td class="negative">-{abs(t[3]):.2f} {data['currency']}</td>'
        f'<td>{t[7]}</td><td>{t[5]}</td></tr>'
        for t in data['expenses'] if t[3] < 0
    )
    
    html_content = html_content.replace('{{ incomes_table }}', incomes_html)
    html_content = html_content.replace('{{ expenses_table }}', expenses_html)
    
    # Сохраняем
    if output_file:
        output_path = config.REPORT_PATH / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return output_path
    
    return html_content 




