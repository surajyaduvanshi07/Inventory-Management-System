import sqlite3
from config import DATABASE_NAME


def get_connection():

    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    return connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT UNIQUE NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS products(

        product_id INTEGER PRIMARY KEY,

        product_name TEXT NOT NULL,

        product_price REAL NOT NULL,

        product_category TEXT NOT NULL

    )

    """)

    connection.commit()

    connection.close()