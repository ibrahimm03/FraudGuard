import sqlite3
from datetime import datetime

# This is the path to our database file
DATABASE = 'fraudguard.db'

def get_connection():
    """Get a connection to the database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    return conn

def create_tables():
    """Create all tables if they don't already exist"""
    conn = get_connection()
    cursor = conn.cursor()

    # Cards table — the credit cards we are monitoring
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT NOT NULL UNIQUE,
            cardholder_name TEXT NOT NULL,
            daily_limit REAL NOT NULL
        )
    ''')

    # Transactions table — every transaction made
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT NOT NULL,
            amount REAL NOT NULL,
            merchant TEXT NOT NULL,
            location TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            is_fraudulent INTEGER DEFAULT 0,
            FOREIGN KEY (card_number) REFERENCES cards (card_number)
        )
    ''')

    # Alerts table — every fraud flag raised
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL,
            reason TEXT NOT NULL,
            severity TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transactions (id)
        )
    ''')