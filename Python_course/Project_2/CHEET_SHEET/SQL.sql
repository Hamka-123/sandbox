/*

КОМПЛЕКТНАЯ ШПАРГАЛКА ПО SQL
Сохраните этот код для быстрого доступа к основным конструкциям SQL

*/

-- ===== 1. ОПЕРАЦИИ ВЫБОРКИ ДАННЫХ (DQL) =====

-- Выбрать все столбцы из таблицы
SELECT * FROM table_name;

-- Выбрать конкретные столбцы
SELECT column1, column2 FROM table_name;

-- Выбрать уникальные значения
SELECT DISTINCT column_name FROM table_name;

-- Выбрать данные с ограничением количества строк
SELECT * FROM table_name LIMIT 10;        -- MySQL, PostgreSQL
SELECT TOP 10 * FROM table_name;          -- SQL Server
SELECT * FROM table_name FETCH FIRST 10 ROWS ONLY; -- Oracle, DB2

-- Фильтрация данных с помощью WHERE
SELECT * FROM table_name 
WHERE condition; -- Используйте: =, !=, <>, <, >, <=, >=, AND, OR, NOT

-- Примеры фильтрации:
WHERE price > 100;
WHERE name = 'Ivan';
WHERE date BETWEEN '2023-01-01' AND '2023-12-31';
WHERE city IN ('Moscow', 'SPb');
WHERE email LIKE '%@gmail.com'; -- % - любая строка, _ - один символ
WHERE phone IS NULL;

-- Сортировка результатов
SELECT * FROM table_name 
ORDER BY column1 ASC,        -- по возрастанию (по умолчанию)
         column2 DESC;       -- по убыванию

-- Группировка и агрегатные функции
SELECT department, 
       COUNT(*) AS emp_count,    -- подсчет строк
       AVG(salary) AS avg_sal,   -- среднее значение
       SUM(sales) AS total_sales,-- сумма
       MIN(age) AS min_age,      -- минимум
       MAX(age) AS max_age       -- максимум
FROM employees 
GROUP BY department
HAVING AVG(salary) > 50000;      -- фильтрация результатов группировки

-- ===== 2. ОПЕРАЦИИ МОДИФИКАЦИИ ДАННЫХ (DML) =====

-- Добавление новых записей
INSERT INTO table_name (column1, column2) 
VALUES (value1, value2);

-- Добавление нескольких записей
INSERT INTO table_name (column1, column2) 
VALUES (value1, value2),
       (value3, value4);

-- Копирование данных из другой таблицы
INSERT INTO table_new (column1, column2)
SELECT col1, col2 FROM table_old;

-- Обновление существующих записей
UPDATE table_name 
SET column1 = new_value1, 
    column2 = new_value2
WHERE condition; -- ВАЖНО: всегда указывайте WHERE!

-- Удаление записей
DELETE FROM table_name 
WHERE condition; -- ВАЖНО: всегда указывайте WHERE!

-- Очистка таблицы (быстрее чем DELETE)
TRUNCATE TABLE table_name;

-- ===== 3. ОПЕРАЦИИ ОПРЕДЕЛЕНИЯ ДАННЫХ (DDL) =====

-- Создание таблицы
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,     -- автоинкремент (MySQL)
    -- id SERIAL PRIMARY KEY,              -- автоинкремент (PostgreSQL)
    -- id INT IDENTITY(1,1) PRIMARY KEY,   -- автоинкремент (SQL Server)
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    age INT CHECK (age >= 0),              -- проверка ограничения
    created_at DATE DEFAULT CURRENT_DATE   -- значение по умолчанию
);
'''
Тип при создании	Хранится как	Описание
INTEGER	            INTEGER	        Целое число (от -2⁶³ до +2⁶³-1).
REAL	            REAL	        Вещественное число (8 байт, double).
TEXT	            TEXT	Строка UTF-8/UTF-16.
BLOB	            BLOB	Двоичные данные "как есть".
NUMERIC	       INTEGER / REAL / TEXT	SQLite сам подбирает хранение.
BOOLEAN	           INTEGER	0 (ложь), 1 (истина).
DATE	        TEXT / REAL / INTEGER	Нет отдельного типа: можно хранить как строку YYYY-MM-DD, как REAL (юлианская дата) или как INTEGER (UNIX timestamp).
DATETIME	    TEXT / REAL / INTEGER	Аналогично DATE.

PRIMARY KEY — уникальный идентификатор.
AUTOINCREMENT — автоувеличение id.
NOT NULL — обязательное поле.
UNIQUE — уникальное значение.
CHECK — условие (например, CHECK(amount > 0)).
DEFAULT — значение по умолчанию.
FOREIGN KEY — связь с другой таблицей.
'''
-- Добавление столбца
ALTER TABLE table_name ADD column_name DATA_TYPE;

-- Удаление столбца
ALTER TABLE table_name DROP COLUMN column_name;

-- Изменение типа столбца
ALTER TABLE table_name ALTER COLUMN column_name TYPE new_data_type; -- PostgreSQL
ALTER TABLE table_name MODIFY column_name new_data_type;           -- MySQL

-- Удаление таблицы
DROP TABLE table_name;

-- ===== 4. СОЕДИНЕНИЯ ТАБЛИЦ (JOINS) =====

/*
ВИЗУАЛИЗАЦИЯ JOIN'ов:
INNER JOIN: только общие записи обеих таблиц
LEFT JOIN: все записи левой таблицы + совпадения правой
RIGHT JOIN: все записи правой таблицы + совпадения левой
FULL JOIN: все записи обеих таблиц
CROSS JOIN: декартово произведение (все со всеми)
*/

-- INNER JOIN (только совпадающие записи)
SELECT * FROM table1
INNER JOIN table2 ON table1.id = table2.table1_id;

-- LEFT JOIN (все из левой + совпадения из правой)
SELECT * FROM table1
LEFT JOIN table2 ON table1.id = table2.table1_id;

-- RIGHT JOIN (все из правой + совпадения из левой)
SELECT * FROM table1
RIGHT JOIN table2 ON table1.id = table2.table1_id;

-- FULL OUTER JOIN (все записи из обеих таблиц)
SELECT * FROM table1
FULL OUTER JOIN table2 ON table1.id = table2.table1_id;

-- CROSS JOIN (декартово произведение)
SELECT * FROM table1 CROSS JOIN table2;

-- ===== 5. РАБОТА СО СТРОКАМИ =====

SELECT 
    LENGTH('text') AS str_length,          -- длина строки
    UPPER('text') AS upper_case,           -- в верхний регистр
    LOWER('TEXT') AS lower_case,           -- в нижний регистр
    TRIM('  text  ') AS trimmed,           -- удаление пробелов по краям
    CONCAT('Hello', ' ', 'World') AS concat, -- объединение строк
    SUBSTRING('Hello', 2, 3) AS substr;    -- подстрока (с позиции 2, 3 символа)

-- ===== 6. РАБОТА С ДАТАМИ =====

SELECT 
    CURRENT_DATE AS current_date,          -- текущая дата
    CURRENT_TIMESTAMP AS current_ts,       -- текущая дата и время
    EXTRACT(YEAR FROM date_column) AS year, -- извлечение года
    DATE_ADD(date_column, INTERVAL 1 DAY) AS next_day, -- добавление дня (MySQL)
    date_column + INTERVAL '1 day' AS next_day_pg; -- добавление дня (PostgreSQL)

-- ===== 7. УСЛОВНЫЕ ВЫРАЖЕНИЯ =====

SELECT 
    CASE 
        WHEN condition1 THEN result1
        WHEN condition2 THEN result2
        ELSE default_result
    END AS case_result,

    COALESCE(NULL, 'default_value') AS coalesce_result, -- первое не-NULL значение
    NULLIF(col1, col2) AS nullif_result;                -- NULL если значения равны

-- ===== 8. ОКОННЫЕ ФУНКЦИИ =====

SELECT 
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank_in_dep,
    AVG(salary) OVER (PARTITION BY department) AS avg_dep_salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num
FROM employees;

-- ===== 9. ОБЩИЕ ТАБЛИЧНЫЕ ВЫРАЖЕНИЯ (CTE) =====

WITH department_stats AS (
    SELECT 
        department, 
        AVG(salary) AS avg_salary,
        COUNT(*) AS emp_count
    FROM employees
    GROUP BY department
)
SELECT * FROM department_stats WHERE avg_salary > 100000;

-- ===== 10. ОСНОВНЫЕ АГРЕГАТНЫЕ ФУНКЦИИ =====

/*
COUNT() - подсчет строк
SUM()   - сумма значений
AVG()   - среднее значение
MIN()   - минимальное значение
MAX()   - максимальное значение
*/

-- ===== 11. ТРАНЗАКЦИИ =====

BEGIN TRANSACTION; -- начало транзакции

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT; -- подтверждение транзакции
-- ROLLBACK; -- отмена транзакции

-- ===== 12. ВАЖНЫЕ ПРИМЕЧАНИЯ =====

/*
1. Всегда используйте WHERE в UPDATE и DELETE
2. Используйте транзакции для важных операций
3. Тестируйте запросы SELECT перед UPDATE/DELETE
4. Обращайте внимание на различия между СУБД
5. Используйте индексы для ускорения запросов
*/

/*
ПРИМЕР РАБОЧЕГО ЗАПРОСА:
SELECT 
    u.name,
    u.email,
    COUNT(o.id) AS order_count,
    SUM(o.amount) AS total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) > 5
ORDER BY total_amount DESC
LIMIT 10;
*/

-- КОНЕЦ ШПАРГАЛКИ --

/*

ПОЛНАЯ ШПАРГАЛКА ПО SQL ТРАНЗАКЦИЯМ
ACID: Atomicity, Consistency, Isolation, Durability

*/

-- ===== 1. БАЗОВЫЙ СИНТАксис ТРАНЗАКЦИЙ =====

-- Начало транзакции (явное)
BEGIN TRANSACTION; -- SQL Server, PostgreSQL
START TRANSACTION; -- MySQL

-- Альтернативные варианты начала
BEGIN; -- Сокращенная форма в PostgreSQL, MySQL
BEGIN WORK;

-- Фиксация (подтверждение) изменений
COMMIT; -- Подтверждаем все изменения
COMMIT TRANSACTION; -- SQL Server

-- Откат (отмена) изменений
ROLLBACK; -- Отменяем все изменения в транзакции
ROLLBACK TRANSACTION; -- SQL Server

-- ===== 2. ПРОСТОЙ ПРИМЕР ТРАНЗАКЦИИ =====

-- Перевод денег между счетами (классический пример)
BEGIN TRANSACTION;

-- Списание со счета отправителя
UPDATE accounts SET balance = balance - 100.00 
WHERE account_id = 123 AND balance >= 100.00;

-- Зачисление на счет получателя
UPDATE accounts SET balance = balance + 100.00 
WHERE account_id = 456;

-- Если оба UPDATE выполнены успешно - фиксируем
COMMIT;

-- Если возникла ошибка - откатываем
-- ROLLBACK;

-- ===== 3. ТРАНЗАКЦИИ С ОБРАБОТКОЙ ОШИБОК =====

-- Для SQL Server
BEGIN TRY
    BEGIN TRANSACTION;
    
    UPDATE accounts SET balance = balance - 100.00 
    WHERE account_id = 123;
    
    UPDATE accounts SET balance = balance + 100.00 
    WHERE account_id = 456;
    
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    ROLLBACK TRANSACTION;
    -- Дополнительная обработка ошибки
    THROW;
END CATCH;

-- Для PostgreSQL
BEGIN;
    UPDATE accounts SET balance = balance - 100.00 
    WHERE account_id = 123;
    
    UPDATE accounts SET balance = balance + 100.00 
    WHERE account_id = 456;
COMMIT;

-- В случае ошибки в PostgreSQL автоматически выполняется ROLLBACK

-- ===== 4. ТОЧКИ СОХРАНЕНИЯ (SAVEPOINT) =====

BEGIN TRANSACTION;

-- Первая операция
UPDATE accounts SET balance = balance - 50.00 
WHERE account_id = 123;

-- Создаем точку сохранения
SAVEPOINT first_operation;

-- Вторая операция
UPDATE accounts SET balance = balance + 50.00 
WHERE account_id = 456;

-- Если вторая операция прошла успешно - фиксируем
COMMIT;

-- Если нужно откатить только вторую операцию
-- ROLLBACK TO SAVEPOINT first_operation;
-- Затем можно продолжить или закоммитить

-- ===== 5. УРОВНИ ИЗОЛЯЦИИ =====

/*
READ UNCOMMITTED - Чтение незафиксированных данных
READ COMMITTED   - Чтение только зафиксированных данных (по умолчанию в большинстве СУБД)
REPEATABLE READ  - Гарантирует повторяемость чтения
SERIALIZABLE     - Полная изоляция, сериализуемое выполнение
*/

-- Установка уровня изоляции для текущей сессии
SET TRANSACTION ISOLATION LEVEL READ COMMITTED; -- SQL Server, PostgreSQL
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ; -- MySQL

-- Установка уровня изоляции для конкретной транзакции
BEGIN TRANSACTION;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Выполнение операций
SELECT * FROM accounts WHERE account_id = 123;
UPDATE accounts SET balance = balance - 100.00 
WHERE account_id = 123;

COMMIT;

-- ===== 6. ПРАКТИЧЕСКИЕ ПРИМЕРЫ =====

-- Пример 1: Безопасное обновление нескольких таблиц
BEGIN TRANSACTION;

UPDATE users SET last_login = GETDATE() 
WHERE user_id = 1;

INSERT INTO login_history (user_id, login_time, ip_address)
VALUES (1, GETDATE(), '192.168.1.1');

COMMIT;

-- Пример 2: Комплексная операция с проверками
BEGIN TRANSACTION;

-- Проверяем достаточно ли денег
IF (SELECT balance FROM accounts WHERE account_id = 123) >= 100.00
BEGIN
    UPDATE accounts SET balance = balance - 100.00 
    WHERE account_id = 123;
    
    UPDATE accounts SET balance = balance + 100.00 
    WHERE account_id = 456;
    
    INSERT INTO transactions (from_acc, to_acc, amount, timestamp)
    VALUES (123, 456, 100.00, GETDATE());
    
    COMMIT;
END
ELSE
BEGIN
    ROLLBACK;
    RAISERROR('Недостаточно средств', 16, 1);
END

-- ===== 7. АВТОКОММИТ РЕЖИМ =====

-- Проверка текущего режима (SQL Server)
SELECT @@AUTCOMMIT; -- 1 = включен, 0 = выключен

-- Выключение автокоммита (не рекомендуется для обычной работы)
SET IMPLICIT_TRANSACTIONS ON; -- SQL Server
SET autocommit = 0; -- MySQL

-- Включение автокоммита (режим по умолчанию)
SET IMPLICIT_TRANSACTIONS OFF; -- SQL Server
SET autocommit = 1; -- MySQL

-- ===== 8. ВЛОЖЕННЫЕ ТРАНЗАКЦИИ =====

-- Проверка уровня вложенности (SQL Server)
SELECT @@TRANCOUNT; -- Возвращает уровень вложенности

BEGIN TRANSACTION; -- @@TRANCOUNT = 1
    -- Некоторые операции...
    BEGIN TRANSACTION; -- @@TRANCOUNT = 2
        -- Внутренние операции...
    COMMIT; -- @@TRANCOUNT = 1
COMMIT; -- @@TRANCOUNT = 0

-- ===== 9. ОСОБЕННОСТИ РАЗНЫХ СУБД =====

-- PostgreSQL: Транзакции автоматически откатываются при ошибках
BEGIN;
    INSERT INTO table1 VALUES (1);
    INSERT INTO table2 VALUES (1); -- Если ошибка здесь
COMMIT; -- Вся транзакция автоматически откатывается

-- MySQL: Необходимо явно обрабатывать ошибки
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
    ROLLBACK;
    RESIGNAL;
END;

START TRANSACTION;
-- операции...
COMMIT;

-- ===== 10. ЛУЧШИЕ ПРАКТИКИ =====

/*
1. Делайте транзакции как можно короче
2. Всегда обрабатывайте ошибки и делайте ROLLBACK
3. Используйте appropriate уровень изоляции
4. Избегайте взаимодействия с пользователем внутри транзакции
5. Тестируйте поведение при конкурентном доступе
6. Используйте логирование для отслеживания транзакций
7. Закрывайте транзакции явно (COMMIT или ROLLBACK)
*/

-- ===== 11. МОНИТОРИНГ ТРАНЗАКЦИЙ =====

-- Просмотр активных транзакций (SQL Server)
SELECT * FROM sys.dm_tran_active_transactions;
SELECT * FROM sys.dm_tran_session_transactions;

-- Просмотр блокировок
SELECT * FROM sys.dm_tran_locks;

-- ===== 12. ШАБЛОН БЕЗОПАСНОЙ ТРАНЗАКЦИИ =====

BEGIN TRY
    BEGIN TRANSACTION;
    
    -- Ваши SQL операции здесь
    -- UPDATE, INSERT, DELETE операции
    
    -- Все прошло успешно
    COMMIT TRANSACTION;
    
END TRY
BEGIN CATCH
    -- Произошла ошибка
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
    
    -- Логируем ошибку
    DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
    DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
    DECLARE @ErrorState INT = ERROR_STATE();
    
    RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
END CATCH;

/*
ПРИМЕР ИСПОЛЬЗОВАНИЯ:
Используйте транзакции для:
- Переводов денег между счетами
- Связанных операций в нескольких таблицах
- Пакетных обновлений, которые должны быть атомарными
- Операций, где важна целостность данных
*/