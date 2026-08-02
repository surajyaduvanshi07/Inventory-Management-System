import os
import resend
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

if not RESEND_API_KEY:
    raise Exception("RESEND_API_KEY not found.")

resend.api_key = RESEND_API_KEY


def send_otp(receiver_email, otp):

    try:

        response = resend.Emails.send({

            "from": "onboarding@resend.dev",

            "to": [receiver_email],

            "subject": "Inventory Management OTP",

            "html": f"""
            <div style="font-family:Arial,sans-serif;padding:20px;">
                <h2>Inventory Management System</h2>

                <p>Hello,</p>

                <p>Your OTP is:</p>

                <h1 style="color:#2563eb;">{otp}</h1>

                <p>This OTP will expire in <b>5 minutes</b>.</p>

                <p>Do not share this OTP with anyone.</p>

                <br>

                <p>Thank you.</p>
            </div>
            """

        })

        print("Email Sent Successfully")
        print(response)

    except Exception as e:

        print("RESEND ERROR:", e)

        raise