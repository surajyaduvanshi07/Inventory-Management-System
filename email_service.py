import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_otp(receiver_email, otp):

    if not EMAIL or not APP_PASSWORD:
        raise Exception(
            "EMAIL or APP_PASSWORD is missing in Environment Variables."
        )

    message = EmailMessage()

    message["Subject"] = "Inventory Management System OTP"

    message["From"] = EMAIL
    message["To"] = receiver_email

    message.set_content(f"""
Hello,

Your One Time Password (OTP) is:

{otp}

This OTP is valid for only 5 minutes.

Do not share this OTP with anyone.

Regards,
Inventory Management System
""")

    try:

        print("Connecting to Gmail SMTP...")

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:

            smtp.ehlo()

            smtp.starttls()

            smtp.ehlo()

            smtp.login(EMAIL, APP_PASSWORD)

            smtp.send_message(message)

        print("OTP sent successfully.")

    except smtplib.SMTPAuthenticationError as e:
        print("SMTP Authentication Error:", e)
        raise Exception(
            "Invalid Gmail Email or App Password."
        )

    except smtplib.SMTPConnectError as e:
        print("SMTP Connection Error:", e)
        raise Exception(
            "Unable to connect to Gmail SMTP."
        )

    except OSError as e:
        print("Network Error:", e)
        raise Exception(
            "Network connection failed while sending email."
        )

    except Exception as e:
        print("Unexpected Error:", e)
        raise