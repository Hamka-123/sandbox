def execute_query(conn, sql, params=None, fetch=False):
    """
    Универсальная функция для выполнения SQL-запроса.

    Args:
        conn: соединение SQLite
        sql: SQL-запрос
        params: кортеж параметров для плейсхолдеров ?
        fetch: bool, если True — возвращает результат (для SELECT)

    Returns:
        list | int | None:
            - list: результаты SELECT
            - int: lastrowid для INSERT
            - int: количество затронутых строк для UPDATE/DELETE
            - None: если не требуется результат
    """
    cursor = conn.cursor()

    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)

    conn.commit()

    if fetch:  # SELECT
        return cursor.fetchall()
    elif sql.strip().upper().startswith("INSERT"):
        return cursor.lastrowid
    else:  # UPDATE / DELETE
        return cursor.rowcount

#-----сбор и обработка пользовательского ввода-------
def title(text):
    print(f"""
    {'-'*20}
    {text}...
    {'-'*20}
    """)

inputs = {
    "db_name": lambda: input("Введите название базы данных: "),
    "table_name": lambda: input("Введите название таблицы: "),
    "columns": lambda: input("Введите поля для таблицы (пример: name, age, email): "),
    "column_for_search": lambda: input("Введите поле для поиска: "),
    "value_for_search": lambda: input("Введите значение для поиска: ")
}

def convert_str_to_dict_for_table(columns_str: str) -> dict:
    """
    Преобразует строку с именами колонок через запятую
    в словарь {column_name: "TEXT"}.
    
    Пример:
        "name, age, email" -> {"name": "TEXT", "age": "TEXT", "email": "TEXT"}
    """
    columns = {}
    for col in columns_str.split(","):
        name = col.strip()
        if name:  # пропускаем пустые
            if name in columns:
                print(f"Внимание: колонка '{name}' уже добавлена, пропускаем дубликат.")
                continue
            columns[name] = "TEXT"
    return columns

def convert_str_to_dict_for_row(values_str: str)-> dict:
    get_table_columns
    pass

