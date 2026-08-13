#user manager with db sqlite3
import json
import pathlib
import sqlite3
#-----config------

USER_FILE_PATH = pathlib.Path(__file__).parent.joinpath("users.json")
DB_NAME = "users"
SQLITE_DATABASE = pathlib.Path(__file__).parent.joinpath(f"{DB_NAME}.db")
DEFAULT_USER_FIELDS = ["name", "age", "email"]
TABLE = "users"


#-----core functions------
def connect_to_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def convert_json_keys_to_db_columns(file):
    fields = get_user_fields(file)
    columns = []
    for f in fields:
        columns.append(f'"{f}" TEXT')   # имя поля + тип (по умолчанию TEXT)
    columns_sql = ",\n".join(columns)
    return columns_sql

def create_db_table(table_name, columns_sql, conn):
    SQL_CREATE_TABLE = f'''
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            {columns_sql}
        );
    '''
    cursor = conn.cursor()
    cursor.execute(SQL_CREATE_TABLE)
    conn.commit()

def read_JSON_file_data(file: pathlib.Path) -> list:
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def get_user_fields(file: pathlib.Path) -> list:
    try:
        data = read_JSON_file_data(file)
        if data:
            return list(data[0].keys())
        else:
            return DEFAULT_USER_FIELDS
    except FileNotFoundError:
        return DEFAULT_USER_FIELDS


def input_user_data(fields: list, existing_data: dict = None) -> dict:
    user_data = {}
    for field in fields:
        default_value = existing_data.get(field) if existing_data else ""
        value = input(f"{field} [{default_value}]: ").strip()
        user_data[field] = value if value else default_value
    return user_data

def import_data_to_db(file: pathlib.Path, table_name: str, conn):
    """Импортирует всех пользователей из JSON в БД"""
    fields = get_user_fields(file)
    data = read_JSON_file_data(file)
    for user in data:
        create_user(table_name, fields, user, conn)
    print(f"✅ Импортировано {len(data)} пользователей в таблицу {table_name}")
    
def get_table_columns(table_name, conn):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns_info = cursor.fetchall()
    # columns_info = [(cid, name, type, notnull, dflt_value, pk), ...]
    columns = [col[1] for col in columns_info]  # берём только имена колонок
    return columns

#-----CRUD functions------
def get_user_by_id(id, table_name, conn) -> tuple:
    SQL_SELECT_USER = f"""
    SELECT * from {table_name}
    WHERE id = '{id}'
    """
    cursor = conn.cursor()
    cursor.execute(SQL_SELECT_USER)
    row = cursor.fetchone()
    return row

def search_user_id_by_name(name, table_name, conn) -> tuple:
    SQL_SELECT_USER_ID = f"""
    SELECT id from {table_name}
    WHERE name = '{name}'
    """
    cursor = conn.cursor()
    cursor.execute(SQL_SELECT_USER_ID)
    row = cursor.fetchone()
    return row[0]

def create_user(table_name, fields, user_data, conn):
    placeholders = ", ".join(["?"] * len(fields))
    columns = ", ".join([f'"{f}"' for f in fields])
    SQL_ADD_USER = f'''
        INSERT INTO "{table_name}" ({columns})
        VALUES ({placeholders})
    '''
    cursor = conn.cursor()
    cursor.execute(SQL_ADD_USER, tuple(user_data[f] for f in fields))
    conn.commit()

def update_user(user_to_update: "id", table_name, conn):
    try:
        if isinstance(user_to_update, int):
            user_id = user_to_update
        elif isinstance(user_to_update, str):
            user_id = search_user_id_by_name(user_to_update, table_name, conn)
            if user_id is None:
                print(f"Пользователь {user_to_update} не найден")
                return
        else:
            raise ValueError("Некорректный аргумент: нужно id (int) или name (str)")

        user = get_user_by_id(user_id, table_name, conn)
        if user is None:
            print(f"Пользователь с id={user_id} не найден")
            return
        
        print("Найден пользователь:", user)
        columns = get_table_columns(table_name, conn)
        user_dict = dict(zip(columns, user))
        
        # Сбор новых данных
        new_user_data = {}
        print("Введите новые значения (Enter — оставить прежнее):")
        for key, old_value in user_dict.items():
            if key == "id":  # id не меняем
                continue
            value = input(f" - {key} : {old_value} ")
            new_user_data[key] = value.strip() if value.strip() else old_value
            
        # Формируем SQL-запрос
        UPDATE_USER = """
            UPDATE {table_name}
            SET {set_clause}
            WHERE id = {user_id};
        """
        set_clause = ", ".join([f"{col} = ?" for col in new_user_data.keys()])
        # подставляем таблицу и готовим SQL
        sql = UPDATE_USER.format(
            table_name=table_name,
            set_clause=set_clause,
            user_id=user_id
        )
        #sql = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
        
        # собираем параметры: все значения + id
        params = list(new_user_data.values())# + [user_id]
        # Выполняем запрос
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        print(f"Пользователь {user_to_update} обновлён ✅")
 
    except Exception as e:
        print("Ошибка при обновлении пользователя:", e)

def delete_user(user_for_delete: "id", table_name, conn):
    try:
        if isinstance(user_for_delete, int):
            user_id = user_for_delete
        elif isinstance(user_for_delete, str):
            user_id = search_user_id_by_name(user_for_delete, table_name, conn)
            if user_id is None:
                print(f"Пользователь {user_for_delete} не найден")
                return
        else:
            raise ValueError("Некорректный аргумент: нужно id (int) или name (str)")

        user = get_user_by_id(user_id, table_name, conn)
        if user is None:
            print(f"Пользователь с id={user_id} не найден")
            return
        
        print("Найден пользователь:", user)
        
        DELETE_USER = """
            DELETE FROM {table_name}
            WHERE id = {user_id};
        """
        # подставляем таблицу и готовим SQL
        sql = DELETE_USER.format(
            table_name=table_name,
            user_id=user_id
        )
        # Выполняем запрос
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    
    except Exception as e:
        print("Ошибка при обновлении пользователя:", e)




#-----main------
if __name__ == "__main__":
    conn = connect_to_db(SQLITE_DATABASE)

    # создаём таблицу
    columns_sql = convert_json_keys_to_db_columns(USER_FILE_PATH)
    create_db_table(TABLE, columns_sql, conn)

    # импортируем данные
    #import_data_to_db(USER_FILE_PATH, TABLE, conn)
    
    #получаем данные
    user = get_user_by_id(1,TABLE, conn)
    print(user)
    
    user_id = search_user_id_by_name("Bentlee", TABLE, conn) #8
    print(user_id)
    
    #меняем данные
    #update_user(8, TABLE, conn)
    update_user("Bentlee", TABLE, conn)
    
    #удаляем данные
    delete_user(8, TABLE, conn)

