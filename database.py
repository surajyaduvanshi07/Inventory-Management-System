import mysql.connector

connection = mysql.connector.connect(
    host = "mysql.railway.internal",
    user = "root",
    password = "jdaBUipZFCNnEmGidEScmarsFxZyissD",
    database = "railway"
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

