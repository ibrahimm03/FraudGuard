import sqlite3
from datetime import datetime

DATABASE = 'fraudguard.db'

def get_connection():
    """Get a connection to the database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create all tables if they don't already exist"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT NOT NULL UNIQUE,
            cardholder_name TEXT NOT NULL,
            daily_limit REAL NOT NULL
        )
    ''')

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

    conn.commit()
    conn.close()

def add_card(card_number, cardholder_name, daily_limit):
    """Add a new card to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cards (card_number, cardholder_name, daily_limit)
        VALUES (?, ?, ?)
    ''', (card_number, cardholder_name, daily_limit))
    conn.commit()
    conn.close()

def add_transaction(card_number, amount, merchant, location, timestamp):
    """Add a new transaction to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (card_number, amount, merchant, location, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (card_number, amount, merchant, location, timestamp))
    transaction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return transaction_id

def get_all_transactions():
    """Get every transaction from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY timestamp DESC')
    transactions = cursor.fetchall()
    conn.close()
    return [dict(t) for t in transactions]

def get_recent_transactions(card_number, limit=10):
    """Get the most recent transactions for a specific card"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions
        WHERE card_number = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (card_number, limit))
    transactions = cursor.fetchall()
    conn.close()
    return [dict(t) for t in transactions]

def flag_transaction(transaction_id):
    """Mark a transaction as fraudulent"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions
        SET is_fraudulent = 1
        WHERE id = ?
    ''', (transaction_id,))
    conn.commit()
    conn.close()

def create_alert(transaction_id, reason, severity, timestamp):
    """Create a fraud alert for a transaction"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alerts (transaction_id, reason, severity, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (transaction_id, reason, severity, timestamp))
    conn.commit()
    conn.close()

def get_all_alerts():
    """Get every alert from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts ORDER BY timestamp DESC')
    alerts = cursor.fetchall()
    conn.close()
    return [dict(a) for a in alerts]