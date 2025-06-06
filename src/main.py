# src/main.py

# Copyright (c) 2025 Liubov Kovaleva (@liuBA29)
# Licensed under the MIT License.


import os
import sqlite3
from src.database import *
from src.document_generator import *
from src.user_input import get_user_input
from tkinter import filedialog, messagebox
from  config import *
import os, sys

def display_options(title, options):
    print(f"\n{title}")
    for option in options:
        print(f"ID: {option[0]}, Данные: {option[1]}")
    print()

def main():
    print(f"Текущий рабочий каталог: {os.getcwd()}")
    print(f"Путь к базе данных: {DB_PATH}")



    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Вывод списка заказчиков
        cursor.execute('SELECT * FROM customers')
        customers = cursor.fetchall()
        display_options("Список заказчиков:", [(row[0], f"{row[1]} (директор: {row[4]})") for row in customers])

        customer_id = int(input("Введите ID клиента: "))
        customer = fetch_customer_data(customer_id)

        # Ввод условий оплаты
        payment_condition = input("Введите тип оплаты (предоплата/постоплата): ").strip().lower()
        completions = fetch_completion_of_work_by_condition(payment_condition)

        if not completions:
            print("Условия оплаты не найдены. Завершение программы.")
            return

        display_options("Список условий оплаты:", [(row[0], row[3]) for row in completions])

        if payment_condition == 'предоплата':
            payments = fetch_all_payment_terms()
            display_options("Список процентов предоплаты:", [(row[0], f"{row[1]}%") for row in payments[1:]])
            term_id = int(input("Введите ID процента предоплаты: "))
            payment = fetch_payment_terms_by_id(term_id)
        else:
            payment = None

        if payment_condition == 'предоплата' and payment is None:
            print("Процент предоплаты не найден. Завершение программы.")
            return

        # Сбор информации для договора
        contract_number, location, doc_date, work_list, total_cost = get_user_input()

        # Генерация документа
        generate_docx(customer, work_list, payment, completions[0], contract_number, location, doc_date, total_cost)

        # if generate_docx.file_path:
        #     print(f"Документ сохранен в папке {generate_docx.file_path} под именем doc_{contract_number}.docx")
        # else:
        #     print("Документ не был сохранен.")

    except ValueError:
        print("Неверный ввод. Пожалуйста, введите целое число для ID.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
