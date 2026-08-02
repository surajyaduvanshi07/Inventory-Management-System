import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

DATABASE_NAME = "inventory.db"

OTP_EXPIRY = 300

SESSION_SECRET_KEY = "inventory_management_secret_key"

APP_NAME = "Inventory Management System"