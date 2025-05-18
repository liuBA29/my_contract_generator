#src/create_db.py
from config import *
import os, sys
import sqlite3


def main():
    # Создаем путь к базе данных
    # db_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print("Создана папка для базы данных:", DATA_DIR)

    #db_path = os.path.join(DATA_DIR, 'customers.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создание таблицы клиентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_name TEXT,
            ruler_name TEXT,
            na_osnovanii TEXT,
            fio_rukovoditelya TEXT,
            address TEXT,
            unp TEXT,
            okpo TEXT,
            rs TEXT,
            dolhnost TEXT,
            short_title TEXT
        )
    ''')
    print("Таблица customers проверена/создана.")

    # Создание таблицы completion_of_work
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completion_of_work (
            completion_id INTEGER PRIMARY KEY,
            completion_date TEXT,
            payment_term_id INTEGER,
            payment_condition TEXT,
            completion_condition TEXT
        )
    ''')
    print("Таблица completion_of_work проверена/создана.")

    # Заполняем таблицу completion_of_work начальными значениями, если она пуста
    cursor.execute('SELECT COUNT(*) FROM completion_of_work')
    count = cursor.fetchone()[0]
    if count == 0:
        values = [
            (0, 'после подписания сторонами настоящего договора', 0, 'постоплата', 'Заказчик производит оплату работ в течение'),
            (1, 'с момента поступления на счет Исполнителя вышеупомянутой предоплаты', 1, 'предоплата', 'Остальную сумму Заказчик обязуется выплатить Исполнителю в течение'),
            (2, 'с момента поступления на счет Исполнителя вышеупомянутой предоплаты', 2, 'предоплата', 'Остальную сумму Заказчик обязуется выплатить Исполнителю в течение'),
            (3, 'с момента поступления на счет Исполнителя вышеупомянутой предоплаты', 3, 'предоплата', None)
        ]
        cursor.executemany('''
            INSERT INTO completion_of_work (completion_id, completion_date, payment_term_id, payment_condition, completion_condition)
            VALUES (?, ?, ?, ?, ?)
        ''', values)
        print("Таблица completion_of_work заполнена начальными значениями.")
    else:
        print("Таблица completion_of_work уже содержит данные (записей:", count, ").")

    # Создание таблицы payment_terms
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_terms (
            term_id INTEGER PRIMARY KEY,
            prepayment_percentage INTEGER,
            remaining_payment INTEGER,
            advance_payment INTEGER
        )
    ''')
    print("Таблица payment_terms проверена/создана.")

    # Заполняем таблицу payment_terms начальными значениями, если она пуста
    cursor.execute('SELECT COUNT(*) FROM payment_terms')
    count = cursor.fetchone()[0]
    if count == 0:
        values = [
            (0, 0, 100, 0),
            (1, 25, 75, 25),
            (2, 50, 50, 50),
            (3, 100, 0, 100)
        ]
        cursor.executemany('''
            INSERT INTO payment_terms (term_id, prepayment_percentage, remaining_payment, advance_payment)
            VALUES (?, ?, ?, ?)
        ''', values)
        print("Таблица payment_terms заполнена начальными значениями.")
    else:
        print("Таблица payment_terms уже содержит данные (записей:", count, ").")

    # Вывод содержимого таблицы completion_of_work
    print("\nСодержимое таблицы completion_of_work:")
    cursor.execute('SELECT * FROM completion_of_work')
    for row in cursor.fetchall():
        print(row)

    # Вывод содержимого таблицы payment_terms
    print("\nСодержимое таблицы payment_terms:")
    cursor.execute('SELECT * FROM payment_terms')
    for row in cursor.fetchall():
        print(row)

    conn.commit()
    conn.close()
    print("\nРабота с базой данных завершена успешно.")

# Вызов функции, если запускать как отдельный скрипт
if __name__ == '__main__':
    main()
