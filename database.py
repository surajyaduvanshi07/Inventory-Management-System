import mysql.connector

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "YOUR_PASSWORD",
    database = "inventory_db"
)

cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS Product(
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_price FLOAT,
    product_category VARCHAR(100)
)
""")

connection.commit()

print("Database Connected Successfully")

