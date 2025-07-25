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

    response = requests.post(url, data=data, headers=headers)
    
    if response.status_code == 200:
        json_resp = response.json()
        if json_resp.get("success"):
            print("✅ Email sent successfully.")
        else:
            print("❌ Failed to send email:", json_resp.get("message"))
    else:
        print(f"❌ HTTP error {response.status_code}: {response.text}")
