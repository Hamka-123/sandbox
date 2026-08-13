import sqlite3
from .constants import *


def start_project():

    match input(display_main_menu()):
        case "0": sys.exit() 
        case "2": 
            test_transaction() 
            pass
        case "3": pass 
        case "4": pass 
        case "5": pass 
        case _: pass 

def display_main_menu(): return MAIN_MENU

def create_database():
    # 
    print ('!!!!!!!!!!!!!!!!!!!!!!!!!!  create db called !!!!!!!!!!!!!!')
    print(DB_NAME)
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(SQL_CREATE_TABLE_CATEGORIES)
        cursor.execute(SQL_CREATE_TABLE_TRANSACTIONS)

        pass
    pass

def  test_transaction() :
    # 
    print(DB_NAME)
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(SQL_TEST_ADD_TRANSACTION)
        cursor.close()
        pass
    pass
