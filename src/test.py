# src/test_customers.py
from src.create_db import main as create_db_main
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
try:
    create_db_main()
except Exception as e:
    messagebox.showerror("Ошибка", f"Ошибка при создании базы данных: {e}")
    exit(1)

from src.database import (fetch_all_customers, fetch_customer_data, fetch_completion_of_work_by_condition,
                          fetch_all_payment_terms, fetch_payment_terms_by_id)
from src.document_generator import generate_docx, generate_docx_act
import add_customer_gui

# --- Глобальные данные ---
customers = fetch_all_customers()




def refresh_customers():
    global customers
    customers = fetch_all_customers()

def open_customer_selector():
    """Открывает окно выбора клиента с поиском"""
    refresh_customers()

    selector = tk.Toplevel(root)
    selector.title("Выбор клиента")
    selector.geometry("400x400")
    selector.grab_set()  # Модальное окно

    tk.Label(selector, text="Поиск клиента (часть имени):").pack(padx=10, pady=5, anchor="w")
    search_var = tk.StringVar()

    entry_search = tk.Entry(selector, textvariable=search_var)
    entry_search.pack(padx=10, pady=5, fill="x")

    listbox = tk.Listbox(selector, height=15)
    listbox.pack(padx=10, pady=5, fill="both", expand=True)

    scrollbar = tk.Scrollbar(listbox, command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    def fill_listbox(filtered=None):
        listbox.delete(0, tk.END)
        data = filtered if filtered is not None else customers
        for cust in data:
            listbox.insert(tk.END, f"{cust[0]} - {cust[1]}")

    fill_listbox()

    def on_search_change(*args):
        term = search_var.get().strip().lower()
        if term == "":
            fill_listbox()
        else:
            filtered = [c for c in customers if term in c[1].lower()]
            fill_listbox(filtered)

    search_var.trace_add('write', on_search_change)

    def on_select(event=None):
        if not listbox.curselection():
            return
        index = listbox.curselection()[0]
        selected = listbox.get(index)
        customer_id = selected.split(" - ")[0]
        entry_customer_id.delete(0, tk.END)
        entry_customer_id.insert(0, customer_id)
        selector.destroy()

    listbox.bind('<Double-Button-1>', on_select)

    btn_select = tk.Button(selector, text="Выбрать", command=on_select)
    btn_select.pack(padx=10, pady=5, anchor="e")

def add_customer():
    add_customer_gui.main()
    refresh_customers()

def generate_act():
    actroot = tk.Toplevel(root)
    actroot.title("Генератор актов")

    tk.Label(actroot, text="Введите дату окончания работ (дд.мм.гггг):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_act_date = tk.Entry(actroot, width=50)
    entry_act_date.grid(row=0, column=1, padx=10, pady=5)

    def on_accept():
        act_date = entry_act_date.get().strip()
        if not act_date:
            messagebox.showerror("Ошибка", "Введите дату окончания работ")
            return

        customer_id = entry_customer_id.get().strip()
        if not customer_id:
            messagebox.showerror("Ошибка", "Введите ID клиента в основном окне")
            return

        try:
            customer_id_int = int(customer_id)
        except ValueError:
            messagebox.showerror("Ошибка", "ID клиента должен быть числом")
            return

        customer = fetch_customer_data(customer_id_int)
        if not customer:
            messagebox.showerror("Ошибка", "Клиент не найден")
            return

        contract_number = entry_contract_number.get().strip()
        if not contract_number:
            messagebox.showerror("Ошибка", "Введите номер договора в основном окне")
            return

        doc_date = entry_doc_date.get().strip()
        if not doc_date:
            messagebox.showerror("Ошибка", "Введите дату договора в основном окне")
            return

        work_list = [child.winfo_children()[0].cget("text") for child in work_entries]

        if not work_list:
            messagebox.showerror("Ошибка", "Введите работы в основном окне")
            return

        try:
            total_cost = float(entry_total_cost.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную стоимость работ в основном окне")
            return

        try:
            file_path = generate_docx_act(customer, list(work_list), contract_number, doc_date, act_date, total_cost)
            if file_path:
                messagebox.showinfo("Успех", f"Акт сохранен: {file_path}")
            actroot.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при генерации акта: {e}")

    generate_button = tk.Button(actroot, text="Принять", command=on_accept)
    generate_button.grid(row=1, column=1, padx=10, pady=10)

def generate_contract():
    try:
        customer_id = entry_customer_id.get().strip()
        if not customer_id:
            messagebox.showerror("Ошибка", "Введите ID клиента")
            return

        customer_id_int = int(customer_id)
        customer = fetch_customer_data(customer_id_int)
        if not customer:
            messagebox.showerror("Ошибка", "Клиент не найден")
            return

        payment_condition = payment_condition_var.get()
        completions = fetch_completion_of_work_by_condition(payment_condition)
        if not completions:
            messagebox.showerror("Ошибка", "Условия оплаты не найдены")
            return
#===================================
        # Если предоплата, то выбираем процент вручную через текстовое поле
        if payment_condition == 'предоплата':
            payment_terms = fetch_all_payment_terms()
            print(f"all-paymeeeents-terms---{payment_terms}")
            prepayment_percentage = payment_term_var.get().strip()
            print(f"prepayment_percentage--{prepayment_percentage}")
            if not prepayment_percentage:
                messagebox.showerror("Ошибка", "Введите процент предоплаты")
                return
            try:
                prepayment_percentage = int(prepayment_percentage)
            except ValueError:
                messagebox.showerror("Ошибка", "Процент предоплаты должен быть числом")
                return

            term_id = None
            for term in payment_terms:
                if term[1] == prepayment_percentage:
                    term_id = term[0]

            payment = fetch_payment_terms_by_id(term_id)
            if payment is None:
                messagebox.showerror("Ошибка", "Процент предоплаты не найден")
                return
        else:
            payment = None

        contract_number = entry_contract_number.get().strip()
        location = entry_location.get().strip()
        doc_date = entry_doc_date.get().strip()
        work_list = [child.winfo_children()[0].cget("text") for child in work_entries]


        try:
            total_cost = float(entry_total_cost.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную стоимость работ")
            return

        file_path = generate_docx(customer, list(work_list), payment, completions[0], contract_number, location,
                                  doc_date,
                                  total_cost)
        if file_path:
            messagebox.showinfo("Успех", f"Документ сохранен: {file_path}")
        else:
            messagebox.showwarning("Отмена", "Сохранение отменено пользователем.")

    except ValueError as e:
        messagebox.showerror("Ошибка", f"Некорректный ввод данных: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

def update_payment_terms(event):
    if payment_condition_var.get() == "предоплата":
        payment_term_combobox.config(state="normal")
        # Получаем все условия оплаты
        payment_terms = fetch_all_payment_terms()
        # Фильтруем условия, исключая те, у которых процент равен 0%
        filtered_payment_terms = [str(row[1]) for row in payment_terms if row[1] > 0]  # Предполагается, что row[1] это процент предоплаты


        payment_term_combobox['values'] = filtered_payment_terms
    else:
        payment_term_combobox.config(state="disabled")
        payment_term_combobox.set('')

def add_work():
    work = entry_work.get().strip()
    if work:
        work_row = tk.Frame(work_frame)
        work_row.pack(fill="x", pady=2)

        label = tk.Label(work_row, text=work, anchor="w")
        label.pack(side="left", fill="x", expand=True)

        def remove():
            work_row.destroy()
            work_entries.remove(work_row)

        remove_button = tk.Button(work_row, text="✖", command=remove, fg="red", bd=0, font=("Arial", 12, "bold"))
        remove_button.pack(side="right")

        work_entries.append(work_row)
        entry_work.delete(0, tk.END)






def refresh_gui():
    refresh_customers()

# --- Создание главного окна ---
root = tk.Tk()
root.title("Генератор договоров")

# Кнопка для открытия окна выбора клиента
tk.Label(root, text="Выберите клиента:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
btn_select_customer = tk.Button(root, text="Выбрать клиента", command=open_customer_selector)
btn_select_customer.grid(row=0, column=1, sticky="w", padx=10, pady=5)

# Кнопка для добавления клиента
add_customer_button = tk.Button(root, text="Добавить клиента", command=add_customer)
add_customer_button.grid(row=0, column=2, padx=10, pady=5)

# Кнопка обновления клиентов
recycle_icon = "🔄"
refresh_button = tk.Button(root, text=f"{recycle_icon}", font=("Arial", 24),
                           width=3, height=1, relief="flat",
                           activebackground="#b2ebf2", borderwidth=0, command=refresh_gui)
refresh_button.grid(row=1, column=2, padx=10, pady=5)

# Поле для ввода ID клиента
tk.Label(root, text="ID клиента:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_customer_id = tk.Entry(root, width=15)
entry_customer_id.grid(row=1, column=1, sticky="w", padx=10, pady=5)

#===================================================


# Поле для ввода номера договора
tk.Label(root, text="Введите номер договора:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_contract_number = tk.Entry(root, width=50)
entry_contract_number.grid(row=2, column=1, padx=10, pady=5)


# Дата договора
tk.Label(root, text="Дата договора (дд.мм.гггг):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_doc_date = tk.Entry(root, width=30)
entry_doc_date.grid(row=3, column=1, sticky="w", padx=10, pady=5)


# Поле для выбора типа оплаты
tk.Label(root, text="Выберите тип оплаты:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
payment_condition_var = tk.StringVar()
payment_condition_combobox = ttk.Combobox(root, textvariable=payment_condition_var, values=["предоплата", "постоплата"],
                                          state="readonly")
payment_condition_combobox.grid(row=4, column=1, padx=10, pady=5)
payment_condition_combobox.bind("<<ComboboxSelected>>", update_payment_terms)


# Поле для выбора процента предоплаты
tk.Label(root, text="Выберите процент предоплаты:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
payment_term_var = tk.StringVar()
payment_term_combobox = ttk.Combobox(root, textvariable=payment_term_var, state="disabled")
payment_term_combobox.grid(row=5, column=1, padx=10, pady=5)



# Поле для ввода места проведения работ
tk.Label(root, text="Введите место проведения работ:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
entry_location = tk.Entry(root, width=50)
entry_location.grid(row=6, column=1, padx=10, pady=5)






tk.Label(root, text="Работы:").grid(row=7, column=0, sticky="nw", padx=10, pady=5)
work_frame = tk.Frame(root)
work_frame.grid(row=7, column=1, columnspan=2, sticky="we", padx=10, pady=5)

# Список для хранения виджетов работ
work_entries = []

# Добавление работы
entry_work = tk.Entry(root, width=30)
entry_work.grid(row=8, column=1, sticky="w", padx=10, pady=5)
btn_add_work = tk.Button(root, text="Добавить работу", command=add_work)
btn_add_work.grid(row=8, column=2, padx=10, pady=5)


# Общая стоимость
tk.Label(root, text="Общая стоимость:").grid(row=9, column=0, sticky="w", padx=10, pady=5)
entry_total_cost = tk.Entry(root, width=30)
entry_total_cost.grid(row=9, column=1, sticky="w", padx=10, pady=5)

# Кнопки генерации
btn_generate_contract = tk.Button(root, text="Генерировать договор", command=generate_contract)
btn_generate_contract.grid(row=10, column=1, sticky="w", padx=10, pady=10)

btn_generate_act = tk.Button(root, text="Генерировать акт", command=generate_act)
btn_generate_act.grid(row=10, column=2, sticky="w", padx=10, pady=10)

root.mainloop()

