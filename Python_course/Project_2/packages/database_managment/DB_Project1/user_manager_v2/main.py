import time
from sqlite_packages import sqlite_connector, sqlite_use_cases, sqlite_tools

if __name__ == "__main__":
    
    MAIN_MENU = '''Select:
    0 - Exit
    # DB CRUD operations
    1 - create database, table
    2 - delete database, table
    3 - edit table
    # DB table data CRUD operations
    4 - add record
    5 - read record
    6 - update record
    7 - delete record
    # Export - import operations (CSV, JSON)
    8 - import table from CSV
    9 - Export data from db
    : '''           

    EDIT_TABLE_MENU = '''Select:
    0 - Return to prev menu
    1 - add column
    2 - delete column
    3 - change all cols names (without id)
    4 - change column definition
    
    '''
    wait = 2
    connect = None  # текущее соединение
    data = None
    
    while True:
        match input(MAIN_MENU):
            
            case "0": break
            
            case "1": 
                sqlite_tools.title("Создание базы данных")
                #1 - create database ✅
                db_name = sqlite_tools.inputs["db_name"]().strip() or "default_db_name"
                sqlite_use_cases.create_db(db_name)
                #1 - create table ✅
                sqlite_tools.title("Создание таблицы")
                connect = sqlite_connector.connect_to_db(db_name)
                table_name = sqlite_tools.inputs["table_name"]().strip() or "default_table_name"
                fields = sqlite_tools.convert_str_to_dict_for_table(sqlite_tools.inputs["columns"]().strip() or "name,age,email")
                columns = {
                    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                    **fields
                }
                sqlite_use_cases.create_table(connect,table_name, columns)
                
            case "2": ## delete database, table ✅
                sqlite_tools.title("Удаление таблицы и базы данных")
                db_name, table_name, connect = sqlite_connector.input_db_and_table_and_connect() 
                sqlite_use_cases.delete_table(connect,table_name)
                sqlite_use_cases.delete_database(db_name)       
                
            case "3":  ##TODO:3 - edit table
                while True:
                    sqlite_tools.title("Изменение таблицы")
                    db_name, table_name, connect = sqlite_connector.input_db_and_table_and_connect() 
                    match input(EDIT_TABLE_MENU):
                        case "0":
                            break
                        case "1":
                            sqlite_use_cases.edit_table(connect, table_name, "add_col")
                            time.sleep(wait)
                            break
                        case "2":
                            sqlite_use_cases.edit_table(connect, table_name, "delete_col")
                            time.sleep(wait)
                            break
                        case "3":
                            sqlite_use_cases.edit_table(connect, table_name, "change_all_col")
                            time.sleep(wait)
                            break
                        case "4":
                            sqlite_use_cases.edit_table(connect, table_name, "change_column_definition")
                            time.sleep(wait)
                            break
                        case _: 
                            print('Something went wrong !!!') 
                            break
                        
            case "4": ##TODO:4 - add record
                sqlite_tools.title("Добавление записи")
                db_name, table_name, connect = sqlite_connector.input_db_and_table_and_connect()      
                
                #input record
                fields = sqlite_tools.convert_str_to_dict_for_row(sqlite_tools.inputs["columns"]().strip() or "name,age,email")
                record = {
                    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                    **fields
                }
                added_record_id = sqlite_use_cases.add_record(connect, table_name, record)
                print(added_record_id)
              
            
            case "5": ##5 - read record ✅
                sqlite_tools.title("Чтение записи")
                db_name, table_name, connect = sqlite_connector.input_db_and_table_and_connect()
                 #input data
                choise = input('''Какие записи хотим получить?
                               1 - Все
                               2 - Одного по полю
                               ''')
                match choise.strip():
                    case "1":
                        result = sqlite_use_cases.read_record(connect, table_name)
                    
                    case "2":
                        column = sqlite_tools.inputs["column_for_search"]().strip() or "id"
                        value = sqlite_tools.inputs["value_for_search"]().strip() or 3
                        result = sqlite_use_cases.read_record(connect, table_name, value, column)
                    case _: 
                        print('Something went wrong !!!') 
                        break
                        
                print(result)                              
                
            case "6": ##TODO:6 - update record
                sqlite_tools.title("Обновление записи")
                db_name, table_name, connect = sqlite_connector.input_db_and_table_and_connect()
                sqlite_use_cases.update_record()
                
            case "7": ##TODO:7 - delete record
                sqlite_tools.title("Удаление записи")
                db_name, table_name, connect = sqlite_connector.input_db_and_table_and_connect()
                sqlite_use_cases.delete_record()
                
            case '8': ##TODO: import_from_csv()
                sqlite_tools.title("Импорт данных")
                file_path = input("Введите путь к файлу: ")
                data = sqlite_use_cases.read_csv_to_dict()
                db_name, table_name, connect = sqlite_connector.input_db_and_table_and_connect()
                sqlite_use_cases.import_data_to_db(connect, table_name, data)
                
            case '9': #9 - Export data from db ✅
                sqlite_tools.title("Экспорт данных")
                db_name, table_name, connect = sqlite_connector.input_db_and_table_and_connect()
                
                data = sqlite_use_cases.export_data_from_db(connect, table_name)
                sqlite_use_cases.save_dict_to_csv(data)
                
            case _: 
                print('Something went wrong !!!') 
                break