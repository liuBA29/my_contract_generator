import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('../data/customers.db')
cursor = conn.cursor()

# Функция для обновления данных клиента
def update_customer():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Ошибка", "Пожалуйста, выберите клиента для редактирования.")
        return

    customer_id = tree.item(selected_item)['values'][0]
    organization_name = entry_organization_name.get()
    ruler_name = entry_ruler_name.get()
    na_osnovanii = entry_na_osnovanii.get()
    fio_rukovoditelya = entry_fio_rukovoditelya.get()
    address = entry_address.get()
    unp = entry_unp.get()
    okpo = entry_okpo.get()
    rs = entry_rs.get()
    dolhnost = entry_dolhnost.get()

    if all([organization_name, ruler_name, na_osnovanii, fio_rukovoditelya, address, unp, okpo, rs, dolhnost]):
        cursor.execute('''
            UPDATE customers 
            SET organization_name=?, ruler_name=?, na_osnovanii=?, fio_rukovoditelya=?, address=?, unp=?, okpo=?, rs=?, dolhnost=?
            WHERE id=?
        ''', (organization_name, ruler_name, na_osnovanii, fio_rukovoditelya, address, unp, okpo, rs, dolhnost, customer_id))
        conn.commit()
        messagebox.showinfo("Успех", "Данные клиента успешно обновлены!")
        load_customers()
        clear_entries()
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

# Функция для загрузки клиентов в таблицу
def load_customers():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM customers")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# Функция для загрузки данных выбранного клиента в поля ввода
def load_customer_data(event):
    selected_item = tree.focus()
    if not selected_item:
        return

    customer_data = tree.item(selected_item)['values']

    entry_organization_name.delete(0, tk.END)
    entry_organization_name.insert(0, customer_data[1])

    entry_ruler_name.delete(0, tk.END)
    entry_ruler_name.insert(0, customer_data[2])

    entry_na_osnovanii.delete(0, tk.END)
    entry_na_osnovanii.insert(0, customer_data[3])

    entry_fio_rukovoditelya.delete(0, tk.END)
    entry_fio_rukovoditelya.insert(0, customer_data[4])

    entry_address.delete(0, tk.END)
    entry_address.insert(0, customer_data[5])

    entry_unp.delete(0, tk.END)
    entry_unp.insert(0, customer_data[6])

    entry_okpo.delete(0, tk.END)
    entry_okpo.insert(0, customer_data[7])

    entry_rs.delete(0, tk.END)
    entry_rs.insert(0, customer_data[8])

    entry_dolhnost.delete(0, tk.END)
    entry_dolhnost.insert(0, customer_data[9])

# Функция для очистки полей ввода
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

# Создаем главное окно
root = tk.Tk()
root.title("Редактирование клиентов")
root.geometry("1200x600")

# Таблица для отображения клиентов
tree = ttk.Treeview(root, columns=('ID', 'Название организации', 'ФИО главы', 'На основании', 'ФИО руководителя', 'Адрес', 'УНП', 'ОКПО', 'Р/счет', 'Должность'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Название организации', text='Название организации')
tree.heading('ФИО главы', text='ФИО главы')
tree.heading('На основании', text='На основании')
tree.heading('ФИО руководителя', text='ФИО руководителя')
tree.heading('Адрес', text='Адрес')
tree.heading('УНП', text='УНП')
tree.heading('ОКПО', text='ОКПО')
tree.heading('Р/счет', text='Р/счет')
tree.heading('Должность', text='Должность')
tree.column('ID', width=30)

# Создаем вертикальную полосу прокрутки
vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.grid(row=0, column=2, sticky='ns')

# Создаем горизонтальную полосу прокрутки
hsb = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
hsb.grid(row=1, column=0, columnspan=2, sticky='ew')

# Размещаем таблицу с привязкой к полосам прокрутки
tree.grid(row=0, column=0, columnspan=2, sticky='nsew')

# Загрузка данных клиента при выборе строки
tree.bind('<<TreeviewSelect>>', load_customer_data)

# Метки и поля ввода для редактирования данных клиента
tk.Label(root, text="Название организации").grid(row=2, column=0, sticky='e')
entry_organization_name = tk.Entry(root)
entry_organization_name.grid(row=2, column=1, sticky='ew')

tk.Label(root, text="ФИО руководителя").grid(row=3, column=0, sticky='e')
entry_fio_rukovoditelya = tk.Entry(root)
entry_fio_rukovoditelya.grid(row=3, column=1, sticky='ew')

tk.Label(root, text="На основании").grid(row=4, column=0, sticky='e')
entry_na_osnovanii = tk.Entry(root)
entry_na_osnovanii.grid(row=4, column=1, sticky='ew')

tk.Label(root, text="ФИО главы организации").grid(row=5, column=0, sticky='e')
entry_ruler_name = tk.Entry(root)
entry_ruler_name.grid(row=5, column=1, sticky='ew')

tk.Label(root, text="Адрес").grid(row=6, column=0, sticky='e')
entry_address = tk.Entry(root)
entry_address.grid(row=6, column=1, sticky='ew')

tk.Label(root, text="УНП").grid(row=7, column=0, sticky='e')
entry_unp = tk.Entry(root)
entry_unp.grid(row=7, column=1, sticky='ew')

tk.Label(root, text="ОКПО").grid(row=8, column=0, sticky='e')
entry_okpo = tk.Entry(root)
entry_okpo.grid(row=8, column=1, sticky='ew')

tk.Label(root, text="Р/счет").grid(row=9, column=0, sticky='e')
entry_rs = tk.Entry(root)
entry_rs.grid(row=9, column=1, sticky='ew')

tk.Label(root, text="Должность").grid(row=10, column=0, sticky='e')
entry_dolhnost = tk.Entry(root)
entry_dolhnost.grid(row=10, column=1, sticky='ew')

# Кнопка для сохранения изменений
tk.Button(root, text="Сохранить изменения", command=update_customer).grid(row=11, column=0, columnspan=2)

# Настройка расширения для колонок и строк
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Загрузка клиентов в таблицу при старте программы
load_customers()

# Запуск основного цикла приложения
root.mainloop()

# Закрытие соединения с базой данных при закрытии приложения
conn.close()

