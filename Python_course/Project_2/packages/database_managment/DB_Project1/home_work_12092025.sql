-- EXECUTING ALL IN 'SQL 1*'
--
-- At line 1:
SELECT * FROM users;
-- Result: 1000 rows returned in 112ms
-- EXECUTING ALL IN 'Simple SELECT'
--
-- At line 1:
SELECT * FROM users;
-- Result: 1000 rows returned in 18ms
-- At line 2:
SELECT * FROM students;
-- Result: 1000 rows returned in 10ms
-- EXECUTING ALL IN 'SQL 2*'
--
-- At line 1:
SELECT first_name, gender FROM users;
-- Result: 1000 rows returned in 41ms
-- EXECUTING ALL IN 'Distinct'
--
-- At line 1:
SELECT DISTINCT gender FROM users;
-- Result: 8 rows returned in 9ms
-- EXECUTING ALL IN 'SQL 2*'
--
-- At line 1:
SELECT first_name, gender FROM users;
-- Result: 1000 rows returned in 12ms
-- At line 2:
SELECT gender FROM users;
-- Result: 1000 rows returned in 20ms
-- EXECUTING ALL IN 'Distinct'
--
-- At line 1:
SELECT DISTINCT gender FROM users;
-- Result: 8 rows returned in 13ms
-- At line 2:
/*
Male
Female
Genderfluid
Polygender
Agender
Non-binary
Genderqueer
Bigender

*/

SELECT count(DISTINCT gender) FROM users;
-- Result: 1 rows returned in 21ms
-- EXECUTING ALL IN 'Aggregate functions*'
--
-- At line 1:
SELECT min(salary) FROM employees;
-- Result: 1 rows returned in 9ms
-- EXECUTING LINE IN 'Aggregate functions*'
--
-- At line 1:
-- 5001
SELECT avg(salary) FROM employees;
-- Result: 1 rows returned in 10ms
-- EXECUTING LINE IN 'Aggregate functions*'
--
-- At line 1:
SELECT min(salary) FROM employees;
-- Result: 1 rows returned in 11ms
-- At line 1:
-- 5001
SELECT avg(salary) FROM employees;
-- Result: 1 rows returned in 12ms
-- EXECUTING LINE IN 'Aggregate functions*'
--
-- At line 1:
SELECT min(salary) FROM employees;
-- Result: 1 rows returned in 8ms
-- At line 1:
-- 5001
SELECT avg(salary) FROM employees;
-- Result: 1 rows returned in 27ms
-- EXECUTING LINE IN 'Aggregate functions*'
--
-- At line 1:
SELECT min(salary) FROM employees;
-- Result: 1 rows returned in 9ms
-- At line 1:
-- -- 5001
SELECT avg(salary) FROM employees;
-- Result: 1 rows returned in 10ms
-- EXECUTING LINE IN 'Aggregate functions*'
--
-- At line 1:
SELECT min(salary) FROM employees;
-- Result: 1 rows returned in 8ms
-- At line 1:
SELECT avg(salary) FROM employees;
-- Result: 1 rows returned in 25ms
-- EXECUTING LINE IN 'Aggregate functions*'
--
-- At line 1:
SELECT avg(salary) FROM employees;
-- Result: 1 rows returned in 16ms
-- EXECUTING LINE IN 'Aggregate functions*'
--
-- At line 1:
SELECT min(salary) FROM employees;
-- Result: 1 rows returned in 9ms
-- At line 1:
SELECT avg(salary) FROM employees;
-- Result: 1 rows returned in 9ms
-- EXECUTING LINE IN 'Aggregate functions*'
--
-- At line 1:
SELECT min(salary) FROM employees;
-- Result: 1 rows returned in 12ms
-- At line 1:
-- 5001
SELECT avg(salary) FROM employees;
-- Result: 1 rows returned in 12ms
-- EXECUTING LINE IN 'Order, limit*'
--
-- At line 1:
SELECT * FROM users
	ORDER by name;
-- Result: no such column: name
-- EXECUTING LINE IN 'Order, limit*'
--
-- At line 1:
SELECT * FROM users
	ORDER by name;
-- Result: no such column: name
-- EXECUTING ALL IN 'Order, limit*'
--
-- At line 1:
SELECT * FROM users ORDER by name;
-- Result: no such column: name
-- EXECUTING ALL IN 'Order, limit*'
--
-- At line 1:
SELECT * FROM users ORDER by name;
-- Result: no such column: name
-- EXECUTING ALL IN 'Order, limit*'
--
-- At line 1:
SELECT * FROM users ORDER BY first_name;
-- Result: 1000 rows returned in 116ms
-- EXECUTING ALL IN 'Order, limit*'
--
-- At line 1:
SELECT * FROM users 
	-- ORDER BY first_name;
	ORDER BY last_name;
-- Result: 1000 rows returned in 16ms
-- EXECUTING LINE IN 'Order, limit*'
--
-- At line 5:
SELECT * FROM employees ORDER by salary;
-- Result: 1000 rows returned in 24ms
-- EXECUTING ALL IN 'Order, limit*'
--
-- At line 1:
SELECT * FROM users 
	-- ORDER BY first_name;
	ORDER BY last_name;
-- Result: 1000 rows returned in 14ms
-- At line 5:
SELECT * FROM employees ORDER by salary;
-- Result: 1000 rows returned in 13ms
-- At line 6:
SELECT * FROM employees ORDER by salary DESC;
-- Result: 1000 rows returned in 24ms
-- EXECUTING ALL IN 'Order, limit*'
--
-- At line 1:
SELECT * FROM users 
	-- ORDER BY first_name;
	ORDER BY last_name;
-- Result: 1000 rows returned in 16ms
-- At line 5:
SELECT * FROM employees ORDER by salary;
-- Result: 1000 rows returned in 14ms
-- At line 6:
SELECT * FROM employees ORDER by salary DESC;
-- Result: 1000 rows returned in 21ms
-- At line 6:
-- ASC, DESC
SELECT * FROM employees LIMIT 10 ORDER
-- Result: near "ORDER": syntax error
-- EXECUTING LINE IN 'Order, limit*'
--
-- At line 6:
-- ASC, DESC
SELECT * FROM employees ORDER by salary DESC LIMIT 10 ;
-- Result: 10 rows returned in 23ms
-- EXECUTING LINE IN 'Order, limit*'
--
-- At line 9:
-- ASC, DESC , first 10 records

SELECT * FROM employees 
	ORDER by salary DESC 
	LIMIT 10 OFFSET 10;
-- Result: 10 rows returned in 20ms
-- EXECUTING LINE IN 'Order, limit*'
--
-- At line 6:
-- ASC, DESC
SELECT * FROM employees 
	ORDER by salary DESC 
	LIMIT 10 ;
-- Result: 10 rows returned in 35ms
-- At line 9:
-- ASC, DESC , first 10 records

SELECT * FROM employees 
	ORDER by salary DESC 
	LIMIT 10 OFFSET 10;
-- Result: 10 rows returned in 20ms
-- EXECUTING LINE IN 'SQL 6*'
--
-- At line 1:
SELECT * FROM employees 
	ORDER by salary DESC 
	LIMIT 10 OFFSET 10;
-- Result: 10 rows returned in 19ms
-- EXECUTING LINE IN 'Order, limit*'
--

-- EXECUTING ALL IN 'Order, limit*'
--
-- At line 1:
SELECT * FROM users 
	-- ORDER BY first_name;
	ORDER BY last_name;
-- Result: 1000 rows returned in 14ms
-- At line 5:
SELECT * FROM employees ORDER by salary;
-- Result: 1000 rows returned in 16ms
-- At line 6:
SELECT * FROM employees ORDER by salary DESC;
-- Result: 1000 rows returned in 16ms
-- At line 6:
-- ASC, DESC
SELECT * FROM employees 
	ORDER by salary DESC 
	LIMIT 10 ;
-- Result: 10 rows returned in 16ms
-- EXECUTING LINE IN 'Aliases*'
--
-- At line 1:
SELECT * FROM employees;
-- Result: 1000 rows returned in 158ms
-- EXECUTING LINE IN 'Aliases*'
--
-- At line 1:
SELECT id as `Employee ID` first_name
-- Result: near "first_name": syntax error
-- EXECUTING ALL IN 'Aliases*'
--
-- At line 1:
SELECT id as 'Employee ID' first_name
-- Result: near "first_name": syntax error
-- EXECUTING ALL IN 'Aliases*'
--
-- At line 1:
SELECT id as 'Employee ID', first_name + " " + last_name AS "Employy name", gender, department FROM employees;
-- Result: 1000 rows returned in 78ms
-- EXECUTING LINE IN 'Aliases*'
--
-- At line 1:
SELECT id as 'Employee ID', first_name + " " + last_name AS "Employy name", gender, department FROM employees LIMIT 10;
-- Result: 10 rows returned in 8ms
-- EXECUTING LINE IN 'Aliases*'
--
-- At line 1:
SELECT id as 'Employee ID', first_name || " " || last_name AS "Employy name", gender, department FROM employees LIMIT 10;
-- Result: 10 rows returned in 9ms
-- EXECUTING LINE IN 'Aliases*'
--
-- At line 1:
SELECT id as 'Employee ID', first_name || " " || last_name AS "Employee name", gender, department FROM employees LIMIT 10;
-- Result: 10 rows returned in 6ms
-- EXECUTING ALL IN 'Simple calculations*'
--
-- At line 1:
SELECT avg(salary) FROM employees;
-- Result: 1 rows returned in 14ms
-- EXECUTING LINE IN 'Simple calculations*'
--
-- At line 1:
-- 10014.497
SELECT first_name, last_name, salary - 10014 FROM employees;
-- Result: 1000 rows returned in 9ms
-- EXECUTING ALL IN 'Grouping*'
--
-- At line 1:
SELECT department, salary FROM employees GROUP by department;
-- Result: 9 rows returned in 15ms
-- EXECUTING ALL IN 'Grouping*'
--
-- At line 1:
SELECT department, sum(salary) FROM employees GROUP by department;
-- Result: 9 rows returned in 6ms
-- EXECUTING LINE IN 'Grouping*'
--
-- At line 2:
SELECT department, min(salary) FROM employees GROUP by department;
-- Result: 9 rows returned in 13ms
-- EXECUTING LINE IN 'Filter: WHERE clause*'
--
-- At line 1:
SELECT * FROM users
	WHERE gender = 'Male'
-- Result: 456 rows returned in 49ms
-- EXECUTING ALL IN 'Filter: WHERE clause*'
--
-- At line 1:
SELECT * FROM users
	-- WHERE gender = 'Male';	
	WHERE gender = 'Genderfluid';
-- Result: 14 rows returned in 11ms
-- EXECUTING LINE IN 'Filter: WHERE clause*'
--
-- At line 5:
/*
Comparison operators
Operator	Meaning				Example
=			equal				age = 25
!= or <>	not equal			age <> 25
>			greater than		salary > 5000
<			less than			salary < 5000
>=			greater or equal	age >= 30
<=			less or equal		age <= 30


Logical operators:
AND
OR 
NOT
*/
SELECT * FROM employees
	WHERE department = 'Marketing' AND salary > 6000;
-- Result: 103 rows returned in 33ms
-- EXECUTING LINE IN 'Filter: WHERE clause*'
--
-- At line 24:
/*
IN
BETWEEN
LIKE
IS NULL
IS NOT NULL
*/	

SELECT * from employees WHERE department IN ('Research and Development (R&D)','Finance');
-- Result: 220 rows returned in 32ms
-- EXECUTING ALL IN 'Filter: WHERE clause*'
--
-- At line 1:
SELECT * FROM users
	-- WHERE gender = 'Male';	
	WHERE gender = 'Genderfluid';
-- Result: 14 rows returned in 42ms
-- At line 5:
/*
Comparison operators
Operator	Meaning				Example
=			equal				age = 25
!= or <>	not equal			age <> 25
>			greater than		salary > 5000
<			less than			salary < 5000
>=			greater or equal	age >= 30
<=			less or equal		age <= 30


Logical operators:
AND
OR 
NOT
*/
SELECT * FROM employees
	WHERE department = 'Marketing' AND salary > 6000;
-- Result: 103 rows returned in 12ms
-- At line 24:
/*
IN
BETWEEN
LIKE
IS NULL
IS NOT NULL
*/	

SELECT * from employees WHERE department IN ('Research and Development (R&D)','Finance');
-- Result: 220 rows returned in 10ms
-- At line 33:
SELECT * from employees WHERE salary BETWEEN 7000 AND 8000;
-- Result: 108 rows returned in 15ms
-- EXECUTING LINE IN 'Filter: WHERE clause*'
--
-- At line 34:
SELECT * from users1 WHERE email IS NULL;
-- Result: 232 rows returned in 43ms
-- EXECUTING ALL IN 'Filter: WHERE clause*'
--
-- At line 1:
SELECT * FROM users
	-- WHERE gender = 'Male';	
	WHERE gender = 'Genderfluid';
-- Result: 14 rows returned in 33ms
-- At line 5:
/*
Comparison operators
Operator	Meaning				Example
=			equal				age = 25
!= or <>	not equal			age <> 25
>			greater than		salary > 5000
<			less than			salary < 5000
>=			greater or equal	age >= 30
<=			less or equal		age <= 30


Logical operators:
AND
OR 
NOT
*/
SELECT * FROM employees
	WHERE department = 'Marketing' AND salary > 6000;
-- Result: 103 rows returned in 3ms
-- At line 24:
/*
IN
BETWEEN
LIKE
IS NULL
IS NOT NULL
*/	

SELECT * from employees WHERE department IN ('Research and Development (R&D)','Finance');
-- Result: 220 rows returned in 9ms
-- At line 33:
SELECT * from employees WHERE salary BETWEEN 7000 AND 8000;
-- Result: 108 rows returned in 12ms
-- At line 34:
SELECT * from users1 WHERE email IS NULL;
-- Result: 232 rows returned in 5ms
-- At line 35:
SELECT * from users1 WHERE email = '';
-- Result: 0 rows returned in 5ms
-- EXECUTING ALL IN 'Filter: WHERE clause*'
--
-- At line 1:
SELECT * FROM users
	-- WHERE gender = 'Male';	
	WHERE gender = 'Genderfluid';
-- Result: 14 rows returned in 31ms
-- At line 5:
/*
Comparison operators
Operator	Meaning				Example
=			equal				age = 25
!= or <>	not equal			age <> 25
>			greater than		salary > 5000
<			less than			salary < 5000
>=			greater or equal	age >= 30
<=			less or equal		age <= 30


Logical operators:
AND
OR 
NOT
*/
SELECT * FROM employees
	WHERE department = 'Marketing' AND salary > 6000;
-- Result: 103 rows returned in 7ms
-- At line 24:
/*
IN
BETWEEN
LIKE
	 % any sequence of any symbols
	 _ one character
IS NULL
IS NOT NULL
*/	

SELECT * from employees WHERE department IN ('Research and Development (R&D)','Finance');
-- Result: 220 rows returned in 7ms
-- At line 35:
SELECT * from employees WHERE salary BETWEEN 7000 AND 8000;
-- Result: 108 rows returned in 18ms
-- At line 36:
SELECT * from users1 WHERE email IS NULL;
-- Result: 232 rows returned in 4ms
-- At line 37:
SELECT * from users1 WHERE ip_address LIKE '117&';
-- Result: 0 rows returned in 8ms
-- EXECUTING ALL IN 'Filter: WHERE clause*'
--
-- At line 1:
SELECT * FROM users
	-- WHERE gender = 'Male';	
	WHERE gender = 'Genderfluid';
-- Result: 14 rows returned in 10ms
-- At line 5:
/*
Comparison operators
Operator	Meaning				Example
=			equal				age = 25
!= or <>	not equal			age <> 25
>			greater than		salary > 5000
<			less than			salary < 5000
>=			greater or equal	age >= 30
<=			less or equal		age <= 30


Logical operators:
AND
OR 
NOT
*/
SELECT * FROM employees
	WHERE department = 'Marketing' AND salary > 6000;
-- Result: 103 rows returned in 4ms
-- At line 24:
/*
IN
BETWEEN
LIKE
	 % any sequence of any symbols
	 _ one character
IS NULL
IS NOT NULL
*/	

SELECT * from employees WHERE department IN ('Research and Development (R&D)','Finance');
-- Result: 220 rows returned in 6ms
-- At line 35:
SELECT * from employees WHERE salary BETWEEN 7000 AND 8000;
-- Result: 108 rows returned in 9ms
-- At line 36:
SELECT * from users1 WHERE email IS NULL;
-- Result: 232 rows returned in 5ms
-- At line 37:
SELECT * from users1 WHERE ip_address LIKE '117%';
-- Result: 4 rows returned in 8ms
-- EXECUTING ALL IN 'Filter: WHERE clause*'
--
-- At line 1:
SELECT * FROM users
	-- WHERE gender = 'Male';	
	WHERE gender = 'Genderfluid';
-- Result: 14 rows returned in 34ms
-- At line 5:
/*
Comparison operators
Operator	Meaning				Example
=			equal				age = 25
!= or <>	not equal			age <> 25
>			greater than		salary > 5000
<			less than			salary < 5000
>=			greater or equal	age >= 30
<=			less or equal		age <= 30


Logical operators:
AND
OR 
NOT
*/
SELECT * FROM employees
	WHERE department = 'Marketing' AND salary > 6000;
-- Result: 103 rows returned in 17ms
-- At line 24:
/*
IN
BETWEEN
LIKE
	 % any sequence of any symbols
	 _ one character
IS NULL
IS NOT NULL
*/	

SELECT * from employees WHERE department IN ('Research and Development (R&D)','Finance');
-- Result: 220 rows returned in 7ms
-- At line 35:
SELECT * from employees WHERE salary BETWEEN 7000 AND 8000;
-- Result: 108 rows returned in 14ms
-- At line 36:
SELECT * from users1 WHERE email IS NULL;
-- Result: 232 rows returned in 9ms
-- At line 37:
SELECT * from users1 WHERE ip_address LIKE '117%';
-- Result: 4 rows returned in 6ms
-- At line 38:
SELECT * from users1 WHERE email LIKE '%@.__';
-- Result: 0 rows returned in 8ms
-- EXECUTING ALL IN 'Filter: WHERE clause*'
--
-- At line 1:
SELECT * FROM users
	-- WHERE gender = 'Male';	
	WHERE gender = 'Genderfluid';
-- Result: 14 rows returned in 32ms
-- At line 5:
/*
Comparison operators
Operator	Meaning				Example
=			equal				age = 25
!= or <>	not equal			age <> 25
>			greater than		salary > 5000
<			less than			salary < 5000
>=			greater or equal	age >= 30
<=			less or equal		age <= 30


Logical operators:
AND
OR 
NOT
*/
SELECT * FROM employees
	WHERE department = 'Marketing' AND salary > 6000;
-- Result: 103 rows returned in 7ms
-- At line 24:
/*
IN
BETWEEN
LIKE
	 % any sequence of any symbols
	 _ one character
IS NULL
IS NOT NULL
*/	

SELECT * from employees WHERE department IN ('Research and Development (R&D)','Finance');
-- Result: 220 rows returned in 4ms
-- At line 35:
SELECT * from employees WHERE salary BETWEEN 7000 AND 8000;
-- Result: 108 rows returned in 4ms
-- At line 36:
SELECT * from users1 WHERE email IS NULL;
-- Result: 232 rows returned in 5ms
-- At line 37:
SELECT * from users1 WHERE ip_address LIKE '117%';
-- Result: 4 rows returned in 5ms
-- At line 38:
SELECT * from users1 WHERE email LIKE '%.__';
-- Result: 173 rows returned in 4ms
-- EXECUTING ALL IN 'Filter: WHERE clause*'
--
-- At line 1:
SELECT * FROM users
	-- WHERE gender = 'Male';	
	WHERE gender = 'Genderfluid';
-- Result: 14 rows returned in 38ms
-- At line 5:
/*
Comparison operators
Operator	Meaning				Example
=			equal				age = 25
!= or <>	not equal			age <> 25
>			greater than		salary > 5000
<			less than			salary < 5000
>=			greater or equal	age >= 30
<=			less or equal		age <= 30


Logical operators:
AND
OR 
NOT
*/
SELECT * FROM employees
	WHERE department = 'Marketing' AND salary > 6000;
-- Result: 103 rows returned in 12ms
-- At line 24:
/*
IN
BETWEEN
LIKE
	 % any sequence of any symbols
	 _ one character
IS NULL
IS NOT NULL
*/	

SELECT * from employees WHERE department IN ('Research and Development (R&D)','Finance');
-- Result: 220 rows returned in 10ms
-- At line 35:
SELECT * from employees WHERE salary BETWEEN 7000 AND 8000;
-- Result: 108 rows returned in 8ms
-- At line 36:
SELECT * from users1 WHERE email IS NULL;
-- Result: 232 rows returned in 11ms
-- At line 37:
SELECT * from users1 WHERE ip_address LIKE '117%';
-- Result: 4 rows returned in 7ms
-- At line 38:
SELECT * from users1 WHERE email LIKE '%.__';
-- Result: 173 rows returned in 4ms
-- At line 39:
SELECT * from users1 WHERE ip_address LIKE '23_.%';
-- Result: 41 rows returned in 5ms
