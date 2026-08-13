import pathlib

## Names
DB_FOLDER = "budget_database"
DB_NAME = "main_db.db"
REPORT_FOLDER = "report"

TABLE_CATEGORIES = "categories"
TABLE_TRANSACTIONS = "transactions"

# User-interface
MAIN_MENU = '''Select action:
0  - Exit
1 - Create transaction
2 - Create category
3 - Get current balance
4 - Get income/expenses report
5 - Get expenses per categories
6 - 
: '''



## SQL queries
SQL_CREATE_TABLE_CATEGORIES = '''
    CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
    );                  
'''

SQL_CREATE_TABLE_TRANSACTIONS = '''
   CREATE TABLE IF NOT EXISTS transactions (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   category_id INTEGER,
   date DATE,
   transactions_amount REAL,
   current_balance REAL CHECK(current_balance > 0),
   comments TEXT,
   FOREIGN KEY (category_id) REFERENCES categories(id)
    );  
'''

SQL_INSERT_TRANSACTION = '''
    INSERT INTO transactions (category_id, date, transactions_amount, current_balance, comments)
    VALUES (?,?,?,?,?);
'''

SQL_INSERT_CATEGORY = '''
    INSERT INTO categories (name)
    VALUES (?);
'''

SQL_SELECT_CATEGORY = '''
SELECT id from categories
where name = ?
'''

SQL_GET_CATEGORIES = '''
SELECT name from categories
'''

SQL_GET_LAST_BALANCE = '''
SELECT current_balance from transactions
ORDER BY date desc
LIMIT 1
'''

GET_TRANSACTIONS_PER_PERIOD = '''
SELECT * from transactions
JOIN categories on transactions.category_id = categories.id
WHERE transactions.date BETWEEN ? AND ?
'''






