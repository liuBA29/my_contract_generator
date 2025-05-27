
# Copyright (c) 2025 Liubov Kovaleva (@liuBA29)
# Licensed under the MIT License.


import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from config import DB_PATH, DATA_DIR
import locale
locale.setlocale(locale.LC_ALL, '')  # Использовать локаль системы, для русской сортировки


def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    conn = sqlite3.connect(DB_PATH)
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
    customer_list = []  # сюда будем сохранять (id, organization_name)

    conn.commit()

    def load_customers():
        listbox_customers.delete(0, tk.END)
        customer_list.clear()
        cursor.execute("SELECT id, organization_name FROM customers")
        rows = cursor.fetchall()
        # Сортируем с учётом локали
        rows.sort(key=lambda x: locale.strxfrm(x[1]))
        for cust_id, cust_name in rows:
            customer_list.append((cust_id, cust_name))
            listbox_customers.insert(tk.END, cust_name)

    def add_customer():
        data = get_entries_data()
        if not all(data.values()):
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")
            return

        cursor.execute('''
            SELECT * FROM customers 
            WHERE LOWER(organization_name) = ? OR LOWER(short_title) = ?
        ''', (data['organization_name'].lower(), data['short_title'].lower()))
        if cursor.fetchone():
            if not messagebox.askyesno("Дубликат",
                                       "Клиент с таким названием или сокращенным названием уже существует. Добавить дубликат?"):
                return

        cursor.execute('''
            INSERT INTO customers (organization_name, ruler_name, na_osnovanii, fio_rukovoditelya, address, unp, okpo, rs, dolhnost, short_title)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(data.values()))
        conn.commit()
        messagebox.showinfo("Успех", "Клиент успешно добавлен!")
        clear_entries()
        load_customers()

    def get_entries_data():
        return {
            'organization_name': entry_organization_name.get(),
            'ruler_name': entry_ruler_name.get(),
            'na_osnovanii': entry_na_osnovanii.get(),
            'fio_rukovoditelya': entry_fio_rukovoditelya.get(),
            'address': entry_address.get(),
            'unp': entry_unp.get(),
            'okpo': entry_okpo.get(),
            'rs': entry_rs.get(),
            'dolhnost': entry_dolhnost.get(),
            'short_title': entry_short_title.get()
        }

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

    def on_customer_select(event):
        if not listbox_customers.curselection():
            return
        index = listbox_customers.curselection()[0]
        customer_id = customer_list[index][0]
        cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
        customer = cursor.fetchone()
        if customer:
            entry_organization_name.delete(0, tk.END)
            entry_organization_name.insert(0, customer[1])
            entry_ruler_name.delete(0, tk.END)
            entry_ruler_name.insert(0, customer[2])
            entry_na_osnovanii.delete(0, tk.END)
            entry_na_osnovanii.insert(0, customer[3])
            entry_fio_rukovoditelya.delete(0, tk.END)
            entry_fio_rukovoditelya.insert(0, customer[4])
            entry_address.delete(0, tk.END)
            entry_address.insert(0, customer[5])
            entry_unp.delete(0, tk.END)
            entry_unp.insert(0, customer[6])
            entry_okpo.delete(0, tk.END)
            entry_okpo.insert(0, customer[7])
            entry_rs.delete(0, tk.END)
            entry_rs.insert(0, customer[8])
            entry_dolhnost.delete(0, tk.END)
            entry_dolhnost.insert(0, customer[9])
            entry_short_title.delete(0, tk.END)
            entry_short_title.insert(0, customer[10])
            root.selected_customer_id = customer_id

    def update_customer():
        if not hasattr(root, 'selected_customer_id'):
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите клиента для редактирования.")
            return
        data = get_entries_data()
        if not all(data.values()):
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")
            return
        cursor.execute('''
            UPDATE customers SET
            organization_name=?,
            ruler_name=?,
            na_osnovanii=?,
            fio_rukovoditelya=?,
            address=?,
            unp=?,
            okpo=?,
            rs=?,
            dolhnost=?,
            short_title=?
            WHERE id=?
        ''', tuple(data.values()) + (root.selected_customer_id,))
        conn.commit()
        messagebox.showinfo("Успех", "Данные клиента обновлены!")
        clear_entries()
        load_customers()
        delattr(root, 'selected_customer_id')

    def delete_customer():
        if not hasattr(root, 'selected_customer_id'):
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите клиента для удаления.")
            return
        if not messagebox.askyesno("Подтверждение", "Вы действительно хотите удалить этого клиента?"):
            return
        cursor.execute("DELETE FROM customers WHERE id=?", (root.selected_customer_id,))
        conn.commit()
        messagebox.showinfo("Успех", "Клиент удален.")
        clear_entries()
        load_customers()
        delattr(root, 'selected_customer_id')

    root = tk.Tk()
    root.title("Управление клиентами")
    root.geometry('900x250')

    tk.Label(root, text="Название организации").grid(row=0, column=0)
    entry_organization_name = tk.Entry(root, width=70)
    entry_organization_name.grid(row=0, column=1)

    tk.Label(root, text="ФИО руководителя (в Род.п.)").grid(row=1, column=0)
    entry_ruler_name = tk.Entry(root, width=70)
    entry_ruler_name.grid(row=1, column=1)

    tk.Label(root, text="На основании (в Род.п.)").grid(row=2, column=0)
    entry_na_osnovanii = tk.Entry(root, width=70)
    entry_na_osnovanii.grid(row=2, column=1)

    tk.Label(root, text="И.О. Фамилия (руководителя)").grid(row=3, column=0)
    entry_fio_rukovoditelya = tk.Entry(root, width=70)
    entry_fio_rukovoditelya.grid(row=3, column=1)

    tk.Label(root, text="Адрес").grid(row=4, column=0)
    entry_address = tk.Entry(root, width=70)
    entry_address.grid(row=4, column=1)

    tk.Label(root, text="УНП").grid(row=5, column=0)
    entry_unp = tk.Entry(root, width=70)
    entry_unp.grid(row=5, column=1)

    tk.Label(root, text="ОКПО").grid(row=6, column=0)
    entry_okpo = tk.Entry(root, width=70)
    entry_okpo.grid(row=6, column=1)

    tk.Label(root, text="Р/счет, банк, S.W.I.F.T. и т.д.").grid(row=7, column=0)
    entry_rs = tk.Entry(root, width=70)
    entry_rs.grid(row=7, column=1)

    tk.Label(root, text="Должность (в Род.п.)").grid(row=8, column=0)
    entry_dolhnost = tk.Entry(root, width=70)
    entry_dolhnost.grid(row=8, column=1)

    tk.Label(root, text="Сокр. название организации").grid(row=9, column=0)
    entry_short_title = tk.Entry(root, width=70)
    entry_short_title.grid(row=9, column=1)

    listbox_customers = tk.Listbox(root, width=45)
    listbox_customers.grid(row=0, column=2, rowspan=10, padx=10, sticky='ns')
    listbox_customers.bind('<<ListboxSelect>>', on_customer_select)

    button_frame = tk.Frame(root)
    button_frame.grid(row=10, column=0, columnspan=5, pady=10)

    tk.Button(button_frame, text="Добавить клиента", command=add_customer).grid(row=0, column=0, padx=15)
    tk.Button(button_frame, text="Редактировать клиента", command=update_customer).grid(row=0, column=1, padx=15)
    tk.Button(button_frame, text="Удалить клиента", command=delete_customer).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Очистить поля", command=clear_entries).grid(row=0, column=3, padx=25)

    load_customers()

    root.mainloop()
    conn.close()


if __name__ == '__main__':
    main()
