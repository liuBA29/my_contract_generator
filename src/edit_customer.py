# crc/edit_customer.py

import tkinter as tk
from tkinter import messagebox
import sqlite3

def main():
    conn = sqlite3.connect('../data/customers.db')
    cursor = conn.cursor()

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

    cursor.execute('SELECT COUNT(*) FROM completion_of_work')
    count = cursor.fetchone()[0]
    if count == 0:
        values = [
            (0, 'после подписания сторонами настоящего договора', 0, 'постоплата',
             'Заказчик производит оплату работ в течение'),
            (1, 'с момента поступления на счет Исполнителя вышеупомянутой предоплаты', 1, 'предоплата',
             'Остальную сумму Заказчик обязуется выплатить Исполнителю в течение'),
            (2, 'с момента поступления на счет Исполнителя вышеупомянутой предоплаты', 2, 'предоплата',
             'Остальную сумму Заказчик обязуется выплатить Исполнителю в течение'),
            (3, 'с момента поступления на счет Исполнителя вышеупомянутой предоплаты', 3, 'предоплата', None)
        ]
        cursor.executemany('''
            INSERT INTO completion_of_work (completion_id, completion_date, payment_term_id, payment_condition, completion_condition)
            VALUES (?, ?, ?, ?, ?)
        ''', values)
        print("Таблица completion_of_work заполнена начальными значениями.")
    else:
        print(f"Таблица completion_of_work уже содержит данные (записей: {count}).")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_terms (
            term_id INTEGER PRIMARY KEY,
            prepayment_percentage INTEGER,
            remaining_payment INTEGER,
            advance_payment INTEGER
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM payment_terms')
    count = cursor.fetchone()[0]

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

    def add_customer():
        organization_name = entry_organization_name.get()
        ruler_name = entry_ruler_name.get()
        na_osnovanii = entry_na_osnovanii.get()
        fio_rukovoditelya = entry_fio_rukovoditelya.get()
        address = entry_address.get()
        unp = entry_unp.get()
        okpo = entry_okpo.get()
        rs = entry_rs.get()
        dolhnost = entry_dolhnost.get()
        short_title = entry_short_title.get()

        if all([organization_name, ruler_name, na_osnovanii, fio_rukovoditelya, address, unp, okpo, rs, dolhnost, short_title]):
            cursor.execute('''
                SELECT * FROM customers 
                WHERE LOWER(organization_name) = LOWER(?) 
                OR LOWER(short_title) = LOWER(?)
            ''', (organization_name, short_title))
            existing_customer = cursor.fetchone()

            if existing_customer:
                response = messagebox.askyesno("Дубликат", "Клиент с таким названием или сокращенным названием уже существует. Добавить дубликат?")
                if not response:
                    return

            cursor.execute('''
                INSERT INTO customers (organization_name, ruler_name, na_osnovanii, fio_rukovoditelya, address, unp, okpo, rs, dolhnost, short_title)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (organization_name, ruler_name, na_osnovanii, fio_rukovoditelya, address, unp, okpo, rs, dolhnost, short_title))
            conn.commit()
            messagebox.showinfo("Успех", "Клиент успешно добавлен!")
            clear_entries()
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

    def clear_entries():
        entry_organization_name.delete(0, tk.END)
        entry_ruler_name.delete(0, tk.END)
        entry_na_osnovanii.delete(0, tk.END)
        entry_fio_rukovoditelya.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_unp.delete(0, tk.END)
        entry_okpo.delete(0, tk.END)
        entry_rs.delete(0, tk.END)
        entry_dolhnost.delete(0, tk.END)
        entry_short_title.delete(0, tk.END)

    root = tk.Tk()
    root.title("Добавление клиентов")
    root.geometry('660x250')

    labels = [
        "Название организации",
        "ФИО руководителя (в Р.п.)",
        "На основании: ",
        "И.О. Фамилия (руководителя)",
        "Адрес",
        "УНП",
        "ОКПО",
        "Р/счет, банк, S.W.I.F.T., адрес банка",
        "Должность (в Р.п.)",
        "Сокращенное название организации"
    ]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(root, text=text).grid(row=i, column=0, sticky='w')
        entry = tk.Entry(root, width=70)
        entry.grid(row=i, column=1)
        entries.append(entry)

    (entry_organization_name, entry_ruler_name, entry_na_osnovanii,
     entry_fio_rukovoditelya, entry_address, entry_unp, entry_okpo,
     entry_rs, entry_dolhnost, entry_short_title) = entries

    tk.Button(root, text="Добавить клиента", command=add_customer).grid(row=10, column=0, columnspan=2, pady=10)

    root.mainloop()

    conn.close()

if __name__ == '__main__':
    main()
