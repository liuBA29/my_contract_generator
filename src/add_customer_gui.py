import tkinter as tk
from tkinter import messagebox
import sqlite3

# Подключаемся к базе данных (если базы нет, то она будет создана)
conn = sqlite3.connect('../data/customers.db')
cursor = conn.cursor()

# Создаем таблицу, если ее нет
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
conn.commit()

# Функция для добавления клиента в базу данных
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

# Создаем главное окно
root = tk.Tk()
root.title("Добавление клиентов")

# Метки и поля ввода
tk.Label(root, text="Название организации").grid(row=0, column=0)
entry_organization_name = tk.Entry(root)
entry_organization_name.grid(row=0, column=1)

tk.Label(root, text="ФИО руководителя").grid(row=1, column=0)
entry_ruler_name = tk.Entry(root)
entry_ruler_name.grid(row=1, column=1)

tk.Label(root, text="На основании").grid(row=2, column=0)
entry_na_osnovanii = tk.Entry(root)
entry_na_osnovanii.grid(row=2, column=1)

tk.Label(root, text="ИО Фамилия главы организации").grid(row=3, column=0)
entry_fio_rukovoditelya = tk.Entry(root)
entry_fio_rukovoditelya.grid(row=3, column=1)

tk.Label(root, text="Адрес").grid(row=4, column=0)
entry_address = tk.Entry(root)
entry_address.grid(row=4, column=1)

tk.Label(root, text="УНП").grid(row=5, column=0)
entry_unp = tk.Entry(root)
entry_unp.grid(row=5, column=1)

tk.Label(root, text="ОКПО").grid(row=6, column=0)
entry_okpo = tk.Entry(root)
entry_okpo.grid(row=6, column=1)

tk.Label(root, text="Р/счет, банк, S.W.I.F.T., адрес банка").grid(row=7, column=0)
entry_rs = tk.Entry(root)
entry_rs.grid(row=7, column=1)

tk.Label(root, text="Должность").grid(row=8, column=0)
entry_dolhnost = tk.Entry(root)
entry_dolhnost.grid(row=8, column=1)


tk.Label(root, text="Сокращенное название организации").grid(row=9, column=0)
entry_short_title = tk.Entry(root)
entry_short_title.grid(row=9, column=1)

# Кнопка для добавления клиента
tk.Button(root, text="Добавить клиента", command=add_customer).grid(row=10, column=0, columnspan=2)

# Запуск основного цикла приложения
root.mainloop()

# Закрытие соединения с базой данных при закрытии приложения
conn.close()
