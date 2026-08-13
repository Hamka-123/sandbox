import pathlib
import sys


# Database structure:

## Names
ROOT_FOLDER = pathlib.Path(sys.argv[0]).parent # caller path
DB_FOLDER = ROOT_FOLDER.joinpath("budget_database")
REPORTS_FOLDER = ROOT_FOLDER.joinpath("reports")
DB_NAME = ROOT_FOLDER.joinpath(DB_FOLDER, "main_db.db")

TABLE_CATEGORIES = "categories"
TABLE_TRANSACTIONS = "transactions"


## SQL queries
SQL_CREATE_TABLE_CATEGORIES = f'''
CREATE TABLE IF NOT EXISTS {TABLE_CATEGORIES} (
	"category_id"	INTEGER,
	"name"	TEXT UNIQUE,
	"remark"	TEXT,
	PRIMARY KEY("category_id" AUTOINCREMENT)
);
'''

SQL_CREATE_TABLE_TRANSACTIONS = f'''
CREATE TABLE  IF NOT EXISTS {TABLE_TRANSACTIONS} (
	"transaction_id"	INTEGER,
	"category_id"	INTEGER,
	"date"	TEXT DEFAULT CURRENT_TIMESTAMP,
	"amount"	REAL,
	"remarks"	TEXT,
	"balance"	REAL CHECK(balance > 0),
	PRIMARY KEY("transaction_id" AUTOINCREMENT),
	FOREIGN KEY("category_id") REFERENCES "categories"("category_id"),
	FOREIGN KEY("date") REFERENCES ""
);
'''

SQL_TEST_ADD_TRANSACTION = f'''
INSERT INTO {TABLE_TRANSACTIONS} 
('amount')
values 
(222)
'''

MAIN_MENU = '''Select action:
0 - Exit
1 - Create database 
2 - Insert test transaction
3 - 
: '''







