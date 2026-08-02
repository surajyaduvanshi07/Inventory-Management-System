import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_otp(receiver_email, otp):

    resend.Emails.send({

        "from": "onboarding@resend.dev",

        "to": receiver_email,

        "subject": "Inventory Management OTP",

        "html": f"""
        <h2>Inventory Management System</h2>

        <p>Your OTP is:</p>

        <h1>{otp}</h1>

        <p>This OTP is valid for 5 minutes.</p>

        <p>Do not share this OTP with anyone.</p>
        """
    })