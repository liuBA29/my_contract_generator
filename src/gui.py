import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.database import (fetch_all_customers, fetch_customer_data, fetch_completion_of_work_by_condition,
                          fetch_all_payment_terms, fetch_payment_terms_by_id)
from src.document_generator import generate_docx

# Функция для генерации договора
def generate_contract():
    try:
        # Получаем данные из полей ввода
        customer_id = entry_customer_id.get().strip()
        if not customer_id:
            messagebox.showerror("Ошибка", "Введите ID клиента")
            return

        customer_id = int(customer_id)
        customer = fetch_customer_data(customer_id)
        if not customer:
            messagebox.showerror("Ошибка", "Клиент не найден")
            return

        payment_condition = payment_condition_var.get()
        completions = fetch_completion_of_work_by_condition(payment_condition)
        if not completions:
            messagebox.showerror("Ошибка", "Условия оплаты не найдены")
            return

        if payment_condition == 'предоплата':
            payment_terms = fetch_all_payment_terms()
            term_id = payment_term_var.get().strip()
            if not term_id:
                messagebox.showerror("Ошибка", "Выберите процент предоплаты")
                return
            term_id = int(term_id)
            payment = fetch_payment_terms_by_id(term_id)
            if payment is None:
                messagebox.showerror("Ошибка", "Процент предоплаты не найден")
                return
        else:
            payment = None

        # Получаем все остальные данные
        contract_number = entry_contract_number.get().strip()
        location = entry_location.get().strip()
        doc_date = entry_doc_date.get().strip()
        work_list = work_listbox.get(0, tk.END)

        try:
            total_cost = float(entry_total_cost.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную стоимость работ")
            return

        # Генерация документа
        generate_docx(customer, list(work_list), payment, completions[0], contract_number, location, doc_date,
                      total_cost)
        messagebox.showinfo("Успех", f"Документ сохранен в папке docs_out под именем contract_{contract_number}.docx")

    except ValueError as e:
        messagebox.showerror("Ошибка", f"Некорректный ввод данных: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

def update_customer_id(event):
    selected_customer = customer_combobox.get()
    if selected_customer:
        customer_id = selected_customer.split(" - ")[0]  # Извлечение ID из строки вида "ID - Name"
        entry_customer_id.delete(0, tk.END)
        entry_customer_id.insert(0, customer_id)

def update_payment_terms(event):
    if payment_condition_var.get() == "предоплата":
        payment_term_combobox.config(state="normal")
        # Загрузить проценты предоплаты
        payment_terms = fetch_all_payment_terms()
        payment_term_combobox['values'] = [str(row[0]) for row in payment_terms]
    else:
        payment_term_combobox.config(state="disabled")
        payment_term_combobox.set('')

# Инициализация главного окна
root = tk.Tk()
root.title("Генератор договоров")

# Поле для выбора клиента
tk.Label(root, text="Выберите клиента:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
customer_combobox = ttk.Combobox(root, width=50, state="readonly")
customer_combobox.grid(row=0, column=1, padx=10, pady=5)

# Заполнение выпадающего списка клиентами
customers = fetch_all_customers()
customer_combobox['values'] = [f"{customer[0]} - {customer[1]}" for customer in customers]
customer_combobox.bind("<<ComboboxSelected>>", update_customer_id)

# Поле для ввода ID клиента (автоматически заполняется при выборе клиента из списка)
tk.Label(root, text="Введите ID клиента:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_customer_id = tk.Entry(root, width=50)
entry_customer_id.grid(row=1, column=1, padx=10, pady=5)

# Поле для выбора типа оплаты
tk.Label(root, text="Выберите тип оплаты:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
payment_condition_var = tk.StringVar()
payment_condition_combobox = ttk.Combobox(root, textvariable=payment_condition_var, values=["предоплата", "постоплата"],
                                          state="readonly")
payment_condition_combobox.grid(row=2, column=1, padx=10, pady=5)

# Поле для выбора процента предоплаты
tk.Label(root, text="Выберите процент предоплаты:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
payment_term_var = tk.StringVar()
payment_term_combobox = ttk.Combobox(root, textvariable=payment_term_var, state="disabled")



payment_term_combobox.grid(row=3, column=1, padx=10, pady=5)

payment_condition_combobox.bind("<<ComboboxSelected>>", update_payment_terms)

# Поле для ввода номера договора
tk.Label(root, text="Введите номер договора:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
entry_contract_number = tk.Entry(root, width=50)
entry_contract_number.grid(row=4, column=1, padx=10, pady=5)

# Поле для ввода места проведения работ
tk.Label(root, text="Введите место проведения работ:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
entry_location = tk.Entry(root, width=50)
entry_location.grid(row=5, column=1, padx=10, pady=5)

# Поле для ввода даты
tk.Label(root, text="Введите дату (дд.мм.гггг):").grid(row=6, column=0, sticky="w", padx=10, pady=5)
entry_doc_date = tk.Entry(root, width=50)
entry_doc_date.grid(row=6, column=1, padx=10, pady=5)

# Поле для ввода работ
tk.Label(root, text="Введите работы:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
entry_work = tk.Entry(root, width=50)
entry_work.grid(row=7, column=1, padx=10, pady=5)

# Список для отображения введенных работ
work_listbox = tk.Listbox(root, width=50, height=5)
work_listbox.grid(row=8, column=1, padx=10, pady=5)

def add_work():
    work = entry_work.get()
    if work:
        work_listbox.insert(tk.END, work)
        entry_work.delete(0, tk.END)

add_work_button = tk.Button(root, text="Добавить работу", command=add_work)
add_work_button.grid(row=7, column=2, padx=10, pady=5)

# Поле для ввода стоимости работ
tk.Label(root, text="Введите стоимость работ (в рублях):").grid(row=9, column=0, sticky="w", padx=10, pady=5)
entry_total_cost = tk.Entry(root, width=50)
entry_total_cost.grid(row=9, column=1, padx=10, pady=5)

# Кнопка для генерации договора
generate_button = tk.Button(root, text="Сгенерировать договор", command=generate_contract)
generate_button.grid(row=10, column=1, padx=10, pady=20)

# Запуск главного окна
root.mainloop()
