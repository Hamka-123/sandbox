import csv
import time
from sqlite_packages import sqlite_connector, sqlite_queries
from sqlite_packages.sqlite_tools import *
import pathlib


def create_db(db_name) -> None:
    sqlite_connector.connect_to_db(f"{db_name}")
    db_file = pathlib.Path(__file__).parent.joinpath(f"{db_name}.db")
    # проверяем, существует ли файл
    if db_file.exists():
        print(f"База данных {db_name} создана ✅")

def create_table(conn, table_name:str, columns:dict) -> str:
    """columns = dict: {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "name": "TEXT"}"""
    params = ",\n    ".join([f"{col} {col_type}" for col, col_type in columns.items()])
    sql = sqlite_queries.CREATE_TABLE.format(table_name=table_name, params=params)
    execute_query(conn, sql)
    print(f"Таблица {table_name} создана ✅")
    return(sql)

def delete_database(db_name):
    db_file = pathlib.Path(__file__).parent.joinpath(f"{db_name}.db")
    # проверяем, существует ли файл
    if db_file.exists():
        db_file.unlink()  # удаляет файл
        print(f"База данных {db_name} удалена ✅")
    else:
        print("Файл базы данных не найден")
        
def delete_table(conn, table_name):
    sql = sqlite_queries.DELETE_TABLE.format(table_name=table_name)
    execute_query(conn, sql)
    print(f"Таблица {table_name} удалена ✅")

def get_table_columns(conn, table_name) -> tuple[list, dict]:
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns_info = cursor.fetchall()
    # columns_info = [(cid, name, type, notnull, dflt_value, pk), ...]
    columns = [col[1] for col in columns_info]  # берём только имена колонок
    columns_types = {col[1]: col[2] for col in columns_info} # Словарь имя_колонки → тип
    return columns, columns_types

def edit_table(conn, table_name, operation):
    if operation == "add_col":
        try:
            column = input("Введите название новой колонки:")
            data_type = input("Введите тип данных в колонке (TEXT, INTEGER, REAL, BLOB, NUMERIC, BOOLEAN, DATE, DATETIME)")
            sql = sqlite_queries.EDIT_TABLE_ADD_COLUMN.format(table_name=table_name, column=column,  data_type=data_type)
            execute_query(conn, sql)
            print(f"Колонка {column} добавлена ✅")
        except Exception as e:
            print("Ошибка при добавлении колонки {column}:", e)

    elif operation == "delete_col":
        try:
            column = input("Введите название колонки для удаления:")
            sql = sqlite_queries.EDIT_TABLE_DELETE_COLUMN.format(table_name=table_name, column=column)
            execute_query(conn, sql)
            print(f"Колонка {column} удалена ✅")
        except Exception as e:
            print("Ошибка при удалении колонки {column}:", e)

    elif operation == "change_all_col":
        try:
            old_columns, old_columns_types = get_table_columns(conn, table_name)
            print("Введите новые названия колонок:")
            old_new_columns_names = {}
            for c in old_columns[1::]:
                new_value = input(f"{c} -> ").strip()
                if new_value == "":
                    new_value = c  # если пользователь ничего не ввёл, оставляем старое имя
                old_new_columns_names[c] = new_value   
            
            fields = {}
            for old_name, new_name in old_new_columns_names.items():
                fields[new_name] = old_columns_types[old_name]  # берём тип из старого словаря      
                
            #создать новую таблицу с новыми колонками
            new_columns = {
                    "id": old_columns_types["id"],
                    **fields
                }
            temp_table_name = f"{table_name}_temp"
            create_table(conn,temp_table_name, new_columns)
            
            #перенести туда данные сравнив колонки
            # 1. Экспортируем данные
            data = export_data_from_db(conn, table_name)
            # 3. Копируем пересекающиеся колонки
            common_cols = set(new_columns.keys()) & set(data[0].keys()) if data else []
            if common_cols:
                for row in data:
                    filtered_row = {col: row[col] for col in common_cols}
                    import_data_to_db(conn, temp_table_name, [filtered_row])    
            #удалить старую таблицу
            execute_query(conn, f'DROP TABLE {table_name};')
            #переименовать новую таблицу в старое имя
            execute_query(conn, f'ALTER TABLE {temp_table_name} RENAME TO {table_name};')
        
        except Exception as e:
            print("Ошибка при изменении колонок {column}:", e)
        
        
    elif operation == "change_column_definition":
        try:
            columns = get_table_columns(conn, table_name)
            #какие колонки хотим поменять?
            #Какие рестрикшены им установить?
            
        except Exception as e:
            print("Ошибка при изменении определения колонок {column}:", e)

def export_data_from_db(conn, table_name) -> list[dict]:
    """
    Экспортирует все данные из таблицы в список словарей.
    """
    columns, _ = get_table_columns(conn, table_name)
    rows = execute_query(conn, sqlite_queries.SELECT_ALL.format(table_name=table_name), fetch=True)
    data = [dict(zip(columns, row)) for row in rows]
    return data

def save_dict_to_csv(data: list[dict]):
    timestamp = int(time.time())
    file_name = f"export_data_{timestamp}.csv"
    path_to_save = pathlib.Path(__file__).parent.joinpath(file_name)
    
    if not data:
        print("Нет данных для сохранения.")
        return
    
    with open(path_to_save, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Данные сохранены в файл {path_to_save} ✅")

def read_csv_to_dict(file_path) -> list[dict]:
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(dict(row))
    return data

def import_data_to_db(conn, table_name, data: list[dict]):
    """
    Импортирует данные (список словарей) в таблицу.
    """
    if not data:
        return
    columns = list(data[0].keys())
    placeholders = ", ".join(["?"] * len(columns))
    cols = ", ".join(columns)
    sql = sqlite_queries.ADD_ONE.format(table_name=table_name, columns = cols, values=placeholders)
    for row in data:
        execute_query(conn, sql, tuple(row[col] for col in columns))


# table data CRUD

def add_record(conn, table_name, record):
    """
    Вставляет одну запись в таблицу.

    Args:
        conn: соединение SQLite
        table_name: имя таблицы
        record: dict, где ключ = колонка, значение = значение
    """
    columns = list(record.keys())
    cols = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(columns))

    sql = sqlite_queries.ADD_ONE.format(
        table_name=table_name,
        columns=cols,
        values=placeholders
    )
    return execute_query(conn, sql, tuple(record[col] for col in columns))

def read_record(conn, table_name, param=None, column="id"):
    """
    Читает записи из таблицы.

    Args:
        conn: соединение SQLite
        table_name: имя таблицы
        param: значение для фильтрации (по умолчанию None = все строки)
        column: имя колонки для фильтрации (по умолчанию 'id')

    Returns:
        list: список кортежей с результатами
    """
    if param is None:  # читать все строки
        sql = sqlite_queries.SELECT_ALL.format(table_name=table_name)
        return execute_query(conn, sql, fetch=True)
    
    # читать одну строку по колонке
    sql = sqlite_queries.SELECT_ONE_BY_COLUMN.format(
        table_name=table_name,
        column=column
    )
    return execute_query(conn, sql, (param,), fetch=True)

def update_record():
    #обновить запись по id
    
    pass

def delete_record():
    
    pass

    
