import sqlite3

def main():
    # Подключаемся к базе данных (если базы нет, то она будет создана)
    conn = sqlite3.connect('../data/customers.db')
    cursor = conn.cursor()

    # Создаем таблицу customers, если ее нет
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

    # Создаем таблицу payment_terms, если ее нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_terms (
            term_id INTEGER PRIMARY KEY,
            prepayment_percentage INTEGER,
            remaining_payment INTEGER,
            advance_payment INTEGER
        )
    ''')

    # Проверяем, есть ли уже записи в payment_terms
    cursor.execute('SELECT COUNT(*) FROM payment_terms')
    count = cursor.fetchone()[0]

    # Если записей нет, добавляем заданные значения
    if count == 0:
        terms = [
            (0, 0, 100, 0),
            (1, 25, 75, 25),
            (2, 50, 50, 50),
            (3, 100, 0, 100)
        ]
        cursor.executemany('''
            INSERT INTO payment_terms (term_id, prepayment_percentage, remaining_payment, advance_payment)
            VALUES (?, ?, ?, ?)
        ''', terms)

    conn.commit()
    conn.close()
