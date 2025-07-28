import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MAILEROO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

def send_verification_email(to_email: str, verification_link: str):
    url = "https://smtp.maileroo.com/send"

    data = {
        "from": SENDER_EMAIL,
        "to": to_email,
        "subject": "Verify your account",
        "plain": f"Hi there!\n\nPlease click the following link to verify your account:\n{verification_link}",
        "html": f"""
            <html>
                <body>
                    <p>Hi there!<br><br>
                    Please click the following link to verify your account:<br>
                    <a href="{verification_link}">Verify my account</a>
                    </p>
                </body>
            </html>
        """,
    }

    headers = {
        "X-API-Key": API_KEY
    }

    requests.post(url, data=data, headers=headers)