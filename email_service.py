import os
import resend
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

resend.api_key = RESEND_API_KEY


def send_otp(receiver_email, otp):

    params = {
        "from": f"Inventory Management <{EMAIL}>",
        "to": [receiver_email],
        "subject": "Inventory Management OTP",
        "html": f"""
        <h2>Inventory Management System</h2>

        <p>Your OTP is:</p>

        <h1>{otp}</h1>

        <p>This OTP will expire in 5 minutes.</p>

        <p>Do not share this OTP with anyone.</p>
        """
    }

    resend.Emails.send(params)