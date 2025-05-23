import sqlite3
import tkinter as tk
from tkinter import messagebox
from config import DB_PATH


def get_customers():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT organization_name FROM customers")
        return [row[0] for row in cursor.fetchall()]


def show_listbox():
    listbox_window.deiconify()
    listbox_window.lift()

def show_all_customers(event=None):
    update_listbox(customer_names)
    show_listbox()


def update_suggestions(event):
    typed = entry_var.get().lower()
    matches = [name for name in customer_names if typed in name.lower()]
    if typed and matches:
        update_listbox(matches)
        show_listbox()
    else:
        hide_listbox()


def update_listbox(names):
    listbox.delete(0, 'end')
    for name in names:
        listbox.insert('end', name)
    listbox.update_idletasks()

    # Изменяем количество видимых строк
    num_visible = min(len(names), 10)  # максимум 10 строк
    listbox.config(height=num_visible)

    # Изменяем размер окна в зависимости от содержимого
    width = listbox.winfo_reqwidth()
    height = listbox.winfo_reqheight()
    x = root.winfo_rootx() + entry.winfo_x()
    y = root.winfo_rooty() + entry.winfo_y() + entry.winfo_height()
    listbox_window.geometry(f"{width}x{height}+{x}+{y}")
    listbox_window.deiconify()
    listbox_window.lift()



def on_listbox_select(event):
    if listbox.curselection():
        index = listbox.curselection()[0]
        selected_name = listbox.get(index)
        entry_var.set(selected_name)
        hide_listbox()


def hide_listbox(event=None):
    listbox_window.withdraw()


def submit():
    name = entry_var.get()
    if name:
        messagebox.showinfo("Выбран клиент", f"Вы выбрали: {name}")
    else:
        messagebox.showwarning("Ошибка", "Введите или выберите имя клиента")


# Основной интерфейс
root = tk.Tk()
root.title("Автоподстановка имени клиента")

tk.Label(root, text="Введите имя клиента:").pack(pady=(10, 0))

entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, width=50)
entry.pack(pady=5)
entry.bind("<KeyRelease>", update_suggestions)
entry.bind("<FocusIn>", show_all_customers)

tk.Button(root, text="Подтвердить", command=submit).pack(pady=10)

# Окно с выпадающим списком
listbox_window = tk.Toplevel(root)
listbox_window.withdraw()
listbox_window.overrideredirect(True)
listbox_window.attributes('-topmost', True)

# Прокрутка
scrollbar = tk.Scrollbar(listbox_window)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(listbox_window, yscrollcommand=scrollbar.set)
listbox.pack(side="left", fill="both", expand=True)
listbox.bind("<<ListboxSelect>>", on_listbox_select)
scrollbar.config(command=listbox.yview)

# Загрузка клиентов
customer_names = get_customers()

def click_outside(event):
    # Получаем абсолютные координаты окна списка и поля ввода
    x_list, y_list = listbox_window.winfo_rootx(), listbox_window.winfo_rooty()
    w_list, h_list = listbox_window.winfo_width(), listbox_window.winfo_height()

    x_entry, y_entry = entry.winfo_rootx(), entry.winfo_rooty()
    w_entry, h_entry = entry.winfo_width(), entry.winfo_height()

    # Координаты клика
    x_click, y_click = event.x_root, event.y_root

    # Проверяем, попадает ли клик в окно списка
    inside_listbox = (x_list <= x_click <= x_list + w_list) and (y_list <= y_click <= y_list + h_list)
    # Проверяем, попадает ли клик в поле ввода
    inside_entry = (x_entry <= x_click <= x_entry + w_entry) and (y_entry <= y_click <= y_entry + h_entry)

    if not inside_listbox and not inside_entry:
        hide_listbox()

# Привязываем обработчик ко всему окну
root.bind("<Button-1>", click_outside)


root.mainloop()
