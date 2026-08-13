import mysql
from mysql import connector

conn = mysql.connector.connect (
    host="host.docker.internal",
    user="root",
    password=""
    
)

if connection.is_connected():
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION();")
    record = cursor.fetchone()
    print(f"Успешное подключение! Версия базы: {record[0]}")
