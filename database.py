import sqlite3
 
DATABASE_NAME = "inventory.db"
 
 
def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection
 
 
def create_table():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            product_price REAL NOT NULL,
            product_category TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()
 
