import sqlite3

def fetch_customer_data(customer_id):
    try:
        conn = sqlite3.connect('data/customers.db')
        c = conn.cursor()
        c.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        customer = c.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    return customer

def fetch_all_payment_terms():
    try:
        conn = sqlite3.connect('data/customers.db')
        c = conn.cursor()
        c.execute('SELECT * FROM payment_terms')
        payment_terms = c.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    return payment_terms

def fetch_completion_of_work():
    try:
        conn = sqlite3.connect('data/customers.db')
        c = conn.cursor()
        c.execute('SELECT * FROM completion_of_work LIMIT 1')
        completion = c.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    return completion
