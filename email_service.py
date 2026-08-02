import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_otp(receiver_email, otp):

    message = EmailMessage()

    message["Subject"] = "Inventory Management OTP"

    message["From"] = EMAIL

    message["To"] = receiver_email

    message.set_content(f"""

Hello,

Your OTP is: {otp}

This OTP will expire in 5 minutes.

Do not share this OTP with anyone.

Inventory Management System

""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(EMAIL, APP_PASSWORD)

        smtp.send_message(message)