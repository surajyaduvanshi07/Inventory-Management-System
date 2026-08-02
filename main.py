from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from database import get_connection, create_tables
from email_service import send_otp
from otp_manager import generate_otp, verify_otp
from models import (
    Product,
    ProductUpdate,
    OTPRequest,
    VerifyOTPRequest
)
from config import (
    APP_NAME,
    SESSION_SECRET_KEY
)

import sqlite3

app = FastAPI(title=APP_NAME)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

create_tables()


@app.get("/")
def login_page(request: Request):

    if request.session.get("logged_in"):

        return RedirectResponse("/dashboard")

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.get("/dashboard")
def dashboard_page(request: Request):

    if not request.session.get("logged_in"):

        return RedirectResponse("/")

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "email": request.session.get("email")
        }
    )


@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse("/")
@app.post("/send-otp")
def send_email_otp(data: OTPRequest):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (data.email,)
    )

    user = cursor.fetchone()

    if user is None:

        cursor.execute(
            """
            INSERT INTO users(email)
            VALUES(?)
            """,
            (data.email,)
        )

        connection.commit()

    connection.close()

    otp = generate_otp(data.email)

    send_otp(
        data.email,
        otp
    )

    return {
        "message": "OTP Sent Successfully"
    }


@app.post("/verify-otp")
def verify_email_otp(
    request: Request,
    data: VerifyOTPRequest
):

    if not verify_otp(
        data.email,
        data.otp
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET last_login=CURRENT_TIMESTAMP
        WHERE email=?
        """,
        (data.email,)
    )

    connection.commit()

    connection.close()

    request.session["logged_in"] = True
    request.session["email"] = data.email

    return {
        "message": "Login Successful"
    }


@app.get("/session")
def session_status(request: Request):

    if request.session.get("logged_in"):

        return {
            "logged_in": True,
            "email": request.session.get("email")
        }

    return {
        "logged_in": False
    }

@app.post("/products", status_code=201)
def add_product(
    request: Request,
    product: Product
):

    if not request.session.get("logged_in"):

        raise HTTPException(
            status_code=401,
            detail="Please Login First"
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT product_id
        FROM products
        WHERE product_id=?
        """,
        (product.product_id,)
    )

    existing_product = cursor.fetchone()

    if existing_product:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Product ID Already Exists"
        )

    cursor.execute(
        """
        INSERT INTO products(
            product_id,
            product_name,
            product_price,
            product_category
        )
        VALUES(?,?,?,?)
        """,
        (
            product.product_id,
            product.product_name,
            product.product_price,
            product.product_category
        )
    )

    connection.commit()

    connection.close()

    return {
        "message": "Product Added Successfully"
    }


@app.get("/products")
def get_all_products(request: Request):

    if not request.session.get("logged_in"):

        raise HTTPException(
            status_code=401,
            detail="Please Login First"
        )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        ORDER BY product_id
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]

@app.get("/products/{product_id}")
def get_product(
    request: Request,
    product_id: int
):

    if not request.session.get("logged_in"):

        raise HTTPException(
            status_code=401,
            detail="Please Login First"
        )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE product_id=?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    connection.close()

    if product is None:

        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return dict(product)


@app.put("/products/{product_id}")
def update_product(
    request: Request,
    product_id: int,
    product: ProductUpdate
):

    if not request.session.get("logged_in"):

        raise HTTPException(
            status_code=401,
            detail="Please Login First"
        )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE product_id=?
        """,
        (product_id,)
    )

    existing_product = cursor.fetchone()

    if existing_product is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    cursor.execute(
        """
        UPDATE products
        SET
            product_name=?,
            product_price=?,
            product_category=?
        WHERE product_id=?
        """,
        (
            product.product_name,
            product.product_price,
            product.product_category,
            product_id
        )
    )

    connection.commit()

    connection.close()

    return {
        "message": "Product Updated Successfully"
    }

@app.delete("/products/{product_id}")
def delete_product(
    request: Request,
    product_id: int
):

    if not request.session.get("logged_in"):

        raise HTTPException(
            status_code=401,
            detail="Please Login First"
        )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE product_id=?
        """,
        (product_id,)
    )

    existing_product = cursor.fetchone()

    if existing_product is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    cursor.execute(
        """
        DELETE FROM products
        WHERE product_id=?
        """,
        (product_id,)
    )

    connection.commit()

    connection.close()

    return {
        "message": "Product Deleted Successfully"
    }


@app.get("/current-user")
def current_user(request: Request):

    if not request.session.get("logged_in"):

        raise HTTPException(
            status_code=401,
            detail="Please Login First"
        )

    return {
        "email": request.session.get("email")
    }


@app.get("/health")
def health():

    return {
        "status": "running",
        "application": APP_NAME
    }

