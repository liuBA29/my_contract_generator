import os
import sqlite3
from src.database import fetch_customer_data, fetch_all_payment_terms, fetch_completion_of_work
from src.document_generator import generate_docx
from src.user_input import get_user_input

def display_options(title, options):
    print(title)
    for option in options:
        print(f"ID: {option[0]}, Данные: {option[1]}")
    print()

def main():
    print(f"Текущий рабочий каталог: {os.getcwd()}")

    DB_PATH = os.path.abspath(os.path.join(os.getcwd(), 'data/customers.db'))
    print(f"Проверка базы данных по пути: {DB_PATH}")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM customers')
        customers = cursor.fetchall()
        display_options("Список заказчиков:", [(row[0], f"{row[1]} (директор: {row[4]})") for row in customers])

        cursor.execute('SELECT * FROM completion_of_work')
        completions = cursor.fetchall()
        display_options("Список условий оплаты:", [(row[0], row[3]) for row in completions])

        cursor.execute('SELECT * FROM payment_terms')
        payments = cursor.fetchall()
        display_options("Список процентов предоплаты:", [(row[0], f"{row[2]}%") for row in payments])

        conn.close()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return

    try:
        customer_id = int(input("Введите ID клиента: "))
        customer = fetch_customer_data(customer_id)

        completion_id = int(input("Введите ID условия оплаты: "))
        completion = fetch_completion_of_work(completion_id)

        term_id = int(input("Введите ID процента предоплаты: "))
        payment = fetch_all_payment_terms(term_id)

        if payment is None:
            print("Условия оплаты не найдены. Завершение программы.")
            return

        contract_number, location, doc_date, work_list, total_cost = get_user_input()

        generate_docx(customer, work_list, payment, completion, contract_number, location, doc_date, total_cost)
        print(f"Документ сохранен в папке docs_out под именем doc_{contract_number}.docx")
    except ValueError:
        print("Неверный ввод. Пожалуйста, введите целое число для ID.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
