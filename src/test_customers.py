# src/gui.py


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
from dotenv import load_dotenv
import os

load_dotenv()



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

    # listbox = tk.Listbox(selector, height=15)
    # listbox.pack(padx=10, pady=5, fill="both", expand=True)

    frame_listbox = tk.Frame(selector)
    frame_listbox.pack(padx=10, pady=5, fill="both", expand=True)

    listbox = tk.Listbox(frame_listbox, height=15)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame_listbox, command=listbox.yview)
    scrollbar.pack(side="right", fill="y")

    listbox.config(yscrollcommand=scrollbar.set)

    def fill_listbox(filtered=None):
        listbox.delete(0, tk.END)
        data = filtered if filtered is not None else customers
        for cust in data:
            listbox.insert(tk.END, f"{cust[0]} - {cust[1]}")

    selector.fill_listbox = fill_listbox  # <<< сохраняем ссылку для внешнего выз
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
        customer_name = selected.split(" - ")[1]

        entry_customer_id.delete(0, tk.END)
        entry_customer_id.insert(0, customer_id)


        label_selected_customer.config(text=f"Вы выбрали: {customer_name}")

        selector.destroy()

    listbox.bind('<Double-Button-1>', on_select)

    btn_select = tk.Button(selector, text="Выбрать", command=on_select)
    btn_select.pack(padx=10, pady=5, anchor="e")

    # сохраняем окно выбора глобально
    global customer_selector_window
    customer_selector_window = selector


def add_customer():
    add_customer_gui.main()
    refresh_customers()
    open_customer_selector()  # Заново открыть окно выбора


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
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Стиль для всего окна
root = tk.Tk()
root.title("Генератор договоров и актов")
root.geometry("600x600")
root.configure(bg="#f9f9f9")  # светлый фон

DEFAULT_FONT = ("Segoe UI", 10)
LABEL_FONT = ("Segoe UI", 10, "bold")
BUTTON_FONT = ("Segoe UI", 10, "bold")

# Общий стиль для Label, Entry, Button
style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="#f9f9f9", font=LABEL_FONT)
style.configure("TEntry", font=DEFAULT_FONT)
style.configure("TButton",
                font=BUTTON_FONT,
                foreground="#ffffff",
                background="#007acc",
                borderwidth=0,
                padding=6)
style.map("TButton",
          foreground=[('active', '#ffffff')],
          background=[('active', '#005f99')])




payment_condition_var = tk.StringVar()
payment_term_var = tk.StringVar()


# Сетка с отступами
def grid_widget(widget, row, col, **kwargs):
    widget.grid(row=row, column=col, sticky="w", padx=12, pady=8, **kwargs)

# Кнопка выбора клиента
lbl_choose_customer = ttk.Label(root, text="Выберите клиента:")
grid_widget(lbl_choose_customer, 0, 0)

btn_select_customer = ttk.Button(root, text="Выбрать клиента", command=open_customer_selector)
grid_widget(btn_select_customer, 0, 1)

label_selected_customer = ttk.Label(root, text="Клиент не выбран", foreground="gray")
label_selected_customer.grid(row=1, column=1, sticky="w", padx=12)

btn_add_customer = ttk.Button(root, text="Добавить клиента", command=add_customer)
btn_add_customer.grid(row=0, column=2, padx=12, pady=8)

btn_refresh = ttk.Button(root, text="⟳", width=3, command=refresh_gui)
# btn_refresh.grid(row=1, column=2, padx=12, pady=8, sticky="w")

# ID клиента (если надо, активируй)
entry_customer_id = ttk.Entry(root, width=15)
# grid_widget(entry_customer_id, 1, 0)

# Номер договора
lbl_contract_number = ttk.Label(root, text="Введите номер договора:")
grid_widget(lbl_contract_number, 2, 0)

entry_contract_number = ttk.Entry(root, width=30)
grid_widget(entry_contract_number, 2, 1)

# Дата договора
lbl_doc_date = ttk.Label(root, text="Дата договора (дд.мм.гггг):")
grid_widget(lbl_doc_date, 3, 0)

entry_doc_date = ttk.Entry(root, width=30)
grid_widget(entry_doc_date, 3, 1)

# Тип оплаты
lbl_payment_condition = ttk.Label(root, text="Выберите тип оплаты:")
grid_widget(lbl_payment_condition, 4, 0)

payment_condition_combobox = ttk.Combobox(root, textvariable=payment_condition_var,
                                         values=["предоплата", "постоплата"],
                                         state="readonly", width=28)
grid_widget(payment_condition_combobox, 4, 1)
payment_condition_combobox.bind("<<ComboboxSelected>>", update_payment_terms)

# Процент предоплаты
lbl_payment_term = ttk.Label(root, text="Выберите процент предоплаты:")
grid_widget(lbl_payment_term, 5, 0)

payment_term_combobox = ttk.Combobox(root, textvariable=payment_term_var, state="disabled", width=28)
grid_widget(payment_term_combobox, 5, 1)




# Поле ввода работ
lbl_work = ttk.Label(root, text="Введите работу:")
grid_widget(lbl_work, 6, 0)

entry_work = ttk.Entry(root, width=30)
grid_widget(entry_work, 6, 1)

btn_add_work = ttk.Button(root, text="Добавить работу", command=add_work)
grid_widget(btn_add_work, 6, 2)

# Фрейм для списка работ с прокруткой
# Фрейм для списка работ с прокруткой (уменьшен в 3 раза)
# Фрейм для списка работ с прокруткой (в 3 раза меньше)
work_frame = tk.Frame(root, bg="#ffffff", relief="sunken", borderwidth=1, height=100)
work_frame.grid(row=7, column=0, columnspan=3, padx=12, pady=8, sticky="ew")
work_frame.grid_propagate(False)  # Отключаем авторастяжение по содержимому

canvas = tk.Canvas(work_frame, bg="#ffffff", highlightthickness=0, height=100)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(work_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

work_list_frame = tk.Frame(canvas, bg="#ffffff")
canvas.create_window((0, 0), window=work_list_frame, anchor='nw')

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

work_list_frame.bind("<Configure>", on_frame_configure)


work_entries = []

# Стоимость работ
lbl_total_cost = ttk.Label(root, text="Общая стоимость работ:")
grid_widget(lbl_total_cost, 8, 0)

entry_total_cost = ttk.Entry(root, width=30)
grid_widget(entry_total_cost, 8, 1)


####=====
# Место проведения работ
lbl_location = ttk.Label(root, text="Место проведения работ:")
grid_widget(lbl_location, 9, 0)

entry_location = ttk.Entry(root, width=30)
grid_widget(entry_location, 9, 1)
####====


# Кнопки генерации документов
btn_generate_contract = ttk.Button(root, text="Сгенерировать договор", command=generate_contract)
btn_generate_contract.grid(row=10, column=0, columnspan=2, pady=15, padx=12, sticky="ew")

btn_generate_act = ttk.Button(root, text="Сгенерировать акт", command=generate_act)
btn_generate_act.grid(row=10, column=2, pady=15, padx=12, sticky="ew")



root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(7, weight=1)

root.mainloop()


