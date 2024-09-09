import os
import sqlite3

def get_db_connection():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/customers.db'))
    print(f"Используемый путь к базе данных: {db_path}")
    conn = sqlite3.connect(db_path)
    return conn

def fetch_customer_data(customer_id):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        customer = c.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    return customer


def fetch_all_customers():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id, organization_name, short_title FROM customers')  # Измените 'customers' на реальное имя вашей таблицы
        customers = c.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    return customers


def fetch_completion_of_work_by_condition(payment_condition):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM completion_of_work WHERE payment_condition = ?', (payment_condition,))
        completions = c.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    return completions

def fetch_all_payment_terms():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM payment_terms')
        payment_terms = c.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    return payment_terms

def fetch_payment_terms_by_id(term_id):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM payment_terms WHERE term_id = ?', (term_id,))
        payment_terms = c.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    return payment_terms


f=fetch_completion_of_work_by_condition("предоплата")
for index, predoplata in enumerate(f, start=0):
    print("fetch_completion_of_work_by_condition [", index,"] =",  predoplata)
print("--", f[0])

ff=fetch_all_payment_terms()

for index, item in enumerate(ff, start=0):
    print("fetch_all_payment_terms [", index, "] =", item)