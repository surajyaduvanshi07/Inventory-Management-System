from pydantic import BaseModel, EmailStr

class Product(BaseModel):
    product_id: int
    product_name: str
    product_price: float
    product_category: str


class ProductUpdate(BaseModel):
    product_name: str
    product_price: float
    product_category: str


class OTPRequest(BaseModel):
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str