import pathlib
import sqlite3
from sqlite_packages import sqlite_tools

def connect_to_db(db_name):
    SQLITE_DATABASE = pathlib.Path(__file__).parent.joinpath(f"{db_name}.db")
    return sqlite3.connect(SQLITE_DATABASE)

def input_db_and_table_and_connect():
    db_name = sqlite_tools.inputs["db_name"]().strip() or "default_db_name"
    table_name = sqlite_tools.inputs["table_name"]().strip() or "default_table_name"
    connect = connect_to_db(db_name)
    return db_name, table_name, connect