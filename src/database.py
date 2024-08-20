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

def fetch_completion_of_work(completion_id):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM completion_of_work WHERE completion_id = ?', (completion_id,))
        completion = c.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    return completion

def fetch_all_payment_terms(term_id):
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