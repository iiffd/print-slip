import sqlite3

conn = sqlite3.connect('orders.db')
cur = conn.cursor()

def make_orders_table():
    # making sqlite tables for keyword phrase
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        order_id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        print_date  TEXT NOT NULL
    )
    ''')

if __name__ == '__main__':
    make_orders_table()
    conn.commit()