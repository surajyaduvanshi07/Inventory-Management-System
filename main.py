from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
import sqlite3
import database

app = FastAPI()

# Static Folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates Folder
templates = Jinja2Templates(directory="templates")


class Product(BaseModel):
    product_id: int
    product_name: str
    product_price: float
    product_category: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(product: Product):

    query = """
    INSERT INTO Product
    (product_id, product_name, product_price, product_category)
    VALUES (?, ?, ?, ?)
    """

    try:
        database.cursor.execute(
            query,
            (
                product.product_id,
                product.product_name,
                product.product_price,
                product.product_category
            )
        )

        database.connection.commit()

        return {
            "message": "Product Added Successfully"
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Product ID Already Exists"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/products")
def get_products():

    query = "SELECT * FROM Product"

    database.cursor.execute(query)

    products = database.cursor.fetchall()

    product_list = []

    for product in products:

        product_list.append({
            "product_id": product[0],
            "product_name": product[1],
            "product_price": product[2],
            "product_category": product[3]
        })

    return product_list


@app.get("/products/{product_id}")
def get_product(product_id: int):

    query = "SELECT * FROM Product WHERE product_id = ?"

    database.cursor.execute(query, (product_id,))

    product = database.cursor.fetchone()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return {
        "product_id": product[0],
        "product_name": product[1],
        "product_price": product[2],
        "product_category": product[3]
    }


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):

    query = """
    UPDATE Product
    SET product_name=?,
        product_price=?,
        product_category=?
    WHERE product_id=?
    """

    database.cursor.execute(
        query,
        (
            product.product_name,
            product.product_price,
            product.product_category,
            product_id
        )
    )

    database.connection.commit()

    if database.cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return {
        "message": "Product Updated Successfully"
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    query = "DELETE FROM Product WHERE product_id = ?"

    database.cursor.execute(query, (product_id,))

    database.connection.commit()

    if database.cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return {
        "message": "Product Deleted Successfully"
    }