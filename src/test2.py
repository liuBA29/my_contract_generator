import sqlite3
import os, sys

def get_table_structure(table_name):
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/customers.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получение структуры таблицы
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    conn.close()

    return columns

# Получение и печать структуры таблицы 'customers'
table_name = 'customers'
columns = get_table_structure(table_name)
print(f"Структура таблицы '{table_name}':")
for column in columns:
    print(f"Имя столбца: {column[1]}, Тип: {column[2]}")
