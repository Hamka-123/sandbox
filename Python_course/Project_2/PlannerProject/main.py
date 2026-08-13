from datetime import datetime
from mybudget.utilities import *

conn = init()
    
while True:
    
    match input(display_main_menu()):
        case "0": break 
        case "1": #1 - Create transaction
            print("Список доступных категорий:" , get_categories(conn))
            category_name = input("Введите название категории: ")
            date = datetime.now()
            transactions_amount = float(input("Введите сумму транзакции (если расход то со знаком '-'): "))
            comments = input("Введите комментарий: ")
            current_balance = calculate_balance(conn, transactions_amount)
            create_transaction(conn, category_name, date, transactions_amount, current_balance, comments)
        case "2": #2 - Create category
            category_name = input("Введите название категории: ")
            create_category(conn, category_name)
        case "3": #3 - Get current balance
            print(get_current_balance(conn))
        case "4": #4 - Get income/expenses report
            start_date = input("Введите дату ОТ (2025-09-01): ") or "2025-09-01"
            end_date = input("Введите дату ДО (2025-09-31): ") or "2025-09-31"
            incomes, expenses = get_inc_exp_data(conn, start_date, end_date)
            print("Incomes: ", convert_tuple_to_dict(incomes))
            print("Expenses: ", convert_tuple_to_dict(expenses))
            save = input("Сохранить в html? y/n:")
            if save.upper() == "Y":
                date = datetime.now().strftime('%Y-%m-%d_%H:%M')
                report_path = generate_report_simple_template(
                    conn=conn,
                    start_date=start_date,
                    end_date=end_date,
                    output_file=f"report_{date}.html"
                ) 
                print("Ваш отчёт тут:", report_path)
                  
        case "5": # 5 - Get expenses per categories
            start_date = input("Введите дату ОТ (2025-09-01): ") or "2025-09-01"
            end_date = input("Введите дату ДО (2025-09-31): ") or "2025-09-31"
            _, expenses = get_inc_exp_data(conn, start_date, end_date)
            expenses_by_category, _ = get_transactions_per_category(expenses)
            print(expenses_by_category)
        case _: break
         
