CREATE TABLE "test_table" (
	"id" INTEGER,
	"name" TEXT,
	"email" TEXT,
	"employment_date" TEXT
);

CREATE TABLE IF NOT EXISTS "test_table" (
"id" INTEGER,
"name" TEXT,
"email" TEXT,
"employment_date" TEXT
);

DROP TABLE IF EXISTS "test_table";

INSERT INTO test_table SELECT id, first_name, email, datetime('now') from employees;

SELECT  * from test_table where email is null;

INSERT INTO test_table (  name, email, employment_date )
VALUES (2,3,datetime('now') );

