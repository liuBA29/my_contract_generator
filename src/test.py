import sqlite3
import os, sys
import tkinter as tk
from tkinter import ttk

# Абсолютный путь к базе данных
DB_PATH = os.path.abspath('../data/customers.db')


def print_table_contents(table_name):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f'SELECT * FROM {table_name}')
        rows = c.fetchall()
        conn.close()

        if rows:
            print(f"Содержимое таблицы {table_name}:")
            for row in rows:
                print(row)
        else:
            print(f"Таблица {table_name} пуста или не существует.")
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")


def main():
    tables = ['customers', 'completion_of_work', 'payment_terms']  # Список таблиц для проверки
    for table in tables:
        print_table_contents(table)



if __name__ == "__main__":
    main()

