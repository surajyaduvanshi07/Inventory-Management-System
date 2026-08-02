import sqlite3

# Database Connection
connection = sqlite3.connect("inventory.db", check_same_thread=False)

# Cursor
cursor = connection.cursor()

print("Database Connected Successfully")

# Create Product Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Product(
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_price REAL NOT NULL,
    product_category TEXT NOT NULL
)
""")

connection.commit()