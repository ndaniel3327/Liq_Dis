import os
import sqlite3

class DBManager:
    def __init__(self, db_path="../products.db"):
        print("Using database at:", os.path.abspath(db_path))
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_products_table()

    def create_products_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                image TEXT
            )
        ''')
        self.conn.commit()

    def get_all_products(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM products')
        return cursor.fetchall()

    def add_product(self, name, price, image):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', (name, price, image))
        self.conn.commit()
