import random
from datetime import datetime, timedelta

otp_storage = {}


def generate_otp(email):

    otp = str(random.randint(100000, 999999))

    otp_storage[email] = {

        "otp": otp,

        "expires": datetime.now() + timedelta(minutes=5)

    }

    return otp


def verify_otp(email, user_otp):

    if email not in otp_storage:

        return False

    data = otp_storage[email]

    if datetime.now() > data["expires"]:

        del otp_storage[email]

        return False

    if data["otp"] == user_otp:

        del otp_storage[email]

        return True

    return False