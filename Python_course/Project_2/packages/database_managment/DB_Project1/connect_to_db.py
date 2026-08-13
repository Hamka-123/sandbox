import sqlite3
import pathlib

SQLITE_DATABASE = pathlib.Path(__file__).parent.joinpath("my_test_db.db")
'''
connection = sqlite3.connect(SQLITE_DATABASE)

print(dir(connection))

cursor = connection.cursor()

print(dir(cursor))
'''
SQL_CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"name"	TEXT,
	"email"	TEXT,
	"employment_date"	TEXT
);
'''
USERS_LIST = [
    ['1','Beatrix','bsmallpeice0@netlog.com','8/5/2025'],
    ['2','Giovanna','gtickel1@seesaa.net','9/15/2024'],
    ['3','Mick','mmahedy2@csmonitor.com','10/10/2024'],
    ['4','Estell','egranleese3@squarespace.com','2/17/2025'],
]
SQL_ADD_USERS_RECORD = '''
INSERT INTO "users"
("id","name","email","employment_date") 
VALUES 
('{}','{}','{}','{}');

'''
with sqlite3.connect(SQLITE_DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute(SQL_CREATE_TABLE)
    for u in USERS_LIST:
        cursor.execute(SQL_ADD_USERS_RECORD.format(*u))
    
    # ДЗ на 16.09
# прикрутить к юзер менеджеру базу данных

#pragma queries sqlite
'''
sqlite3 (модуль)
│
├─ connect(database, ...) → Connection
│      # Открывает соединение с базой данных, возвращает объект Connection
├─ complete_statement(sql)
│      # Проверяет, завершено ли SQL-выражение
├─ register_adapter(type, callable)
│      # Регистрирует адаптер Python → SQL
├─ register_converter(name, callable)
│      # Регистрирует конвертер SQL → Python
│
└─ Connection (conn)
    │
    ├─ cursor() → Cursor
    │      # Создаёт объект Cursor для выполнения SQL-запросов
    ├─ commit()
    │      # Сохраняет изменения в базе данных
    ├─ rollback()
    │      # Откатывает текущую транзакцию
    ├─ close()
    │      # Закрывает соединение с базой
    ├─ execute(sql, params=None)
    │      # Выполняет один SQL-запрос (короткий путь через Connection)
    ├─ executemany(sql, seq_of_params)
    │      # Выполняет один SQL-запрос для набора параметров
    ├─ executescript(sql_script)
    │      # Выполняет несколько SQL-команд сразу
    ├─ create_function(name, num_params, func)
    │      # Создаёт пользовательскую SQL-функцию на Python
    ├─ create_aggregate(name, num_params, aggregate_class)
    │      # Регистрирует агрегатную функцию
    ├─ create_collation(name, callable)
    │      # Регистрирует пользовательскую функцию сравнения строк
    └─ interrupt()
           # Прерывает выполнение запросов

    Cursor (cursor)
    │
    ├─ execute(sql, params=None)
    │      # Выполняет SQL-запрос с параметрами
    ├─ executemany(sql, seq_of_params)
    │      # Выполняет SQL-запрос для множества наборов параметров
    ├─ executescript(sql_script)
    │      # Выполняет несколько SQL-команд из строки
    ├─ fetchone()
    │      # Возвращает одну строку результата (или None)
    ├─ fetchall()
    │      # Возвращает все строки результата
    ├─ fetchmany(size=arraysize)
    │      # Возвращает указанное количество строк
    ├─ close()
    │      # Закрывает курсор
    │
    ├─ Свойства:
    │    ├─ description
    │    │      # Список кортежей с описанием колонок последнего запроса
    │    ├─ rowcount
    │    │      # Количество затронутых последним запросом строк
    │    └─ lastrowid
    │           # ID последней вставленной строки (для AUTOINCREMENT)
    └─ arraysize
           # Размер выборки по умолчанию для fetchmany()

'''

'''
 ├── DatabaseError
 │    ├── IntegrityError
 │    ├── ProgrammingError
 │    ├── DataError
 │    └── OperationalError
 ├── InterfaceError
 ├── NotSupportedError
'''