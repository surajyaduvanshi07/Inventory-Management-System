from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from email_service import send_otp
from otp_manager import generate_otp, verify_otp
import sqlite3

 
from database import get_connection, create_table
verify_emails = set()
 
app = FastAPI(title="Inventory Management System")
 
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
 
create_table()
 
 
class Product(BaseModel):
    product_id: int
    product_name: str
    product_price: float
    product_category: str

class OTPRequest(BaseModel):
    email: str


class VerifyOTPRequest(BaseModel):
    email: str
    otp: str
 
 
class ProductUpdate(BaseModel):
    product_name: str
    product_price: float
    product_category: str
 
 
@app.get("/")
def read_index(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={}
    )
 
@app.post("/products", status_code=201)
def add_product(product: Product):

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT product_id FROM Product WHERE product_id = ?",
            (product.product_id,),
        )
        existing_product = cursor.fetchone()
        if existing_product:
            raise HTTPException(status_code=400, detail="Duplicate Product ID")
 
        cursor.execute(
            """
            INSERT INTO Product (product_id, product_name, product_price, product_category)
            VALUES (?, ?, ?, ?)
            """,
            (
                product.product_id,
                product.product_name,
                product.product_price,
                product.product_category,
            ),
        )
        connection.commit()
        return {"message": "Product Added Successfully"}
    except HTTPException:
        raise
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        connection.close()
 
 
@app.get("/products")
def get_all_products():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Product")
        rows = cursor.fetchall()
        products = [dict(row) for row in rows]
        return products
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        connection.close()
 
 
@app.get("/products/{product_id}")
def get_product(product_id: int):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM Product WHERE product_id = ?", (product_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Product Not Found")
        return dict(row)
    except HTTPException:
        raise
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        connection.close()
 
 
@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT product_id FROM Product WHERE product_id = ?", (product_id,)
        )
        existing_product = cursor.fetchone()
        if existing_product is None:
            raise HTTPException(status_code=404, detail="Product Not Found")
 
        cursor.execute(
            """
            UPDATE Product
            SET product_name = ?, product_price = ?, product_category = ?
            WHERE product_id = ?
            """,
            (
                product.product_name,
                product.product_price,
                product.product_category,
                product_id,
            ),
        )
        connection.commit()
        return {"message": "Product Updated Successfully"}
    except HTTPException:
        raise
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        connection.close()
 
 
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT product_id FROM Product WHERE product_id = ?", (product_id,)
        )
        existing_product = cursor.fetchone()
        if existing_product is None:
            raise HTTPException(status_code=404, detail="Product Not Found")
 
        cursor.execute("DELETE FROM Product WHERE product_id = ?", (product_id,))
        connection.commit()
        return {"message": "Product Deleted Successfully"}
    except HTTPException:
        raise
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        connection.close()

@app.post("/send-otp")
def send_email_otp(data: OTPRequest):

    email = data.email

    otp = generate_otp(email)

    send_otp(email, otp)

    return {

        "message": "OTP Sent Successfully"

    }

@app.post("/verify-otp")
def verify_email_otp(data: VerifyOTPRequest):

    email = data.email
    otp = data.otp

    if verify_otp(email, otp):

        verify_emails.add(email)

        return {

            "message": "OTP Verified Successfully"

        }

    raise HTTPException(

        status_code=400,

        detail="Invalid OTP"

    )