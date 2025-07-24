import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

def send_verification_email(to_email: str, verification_link: str):
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("PASSWORD")


    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your account"
    message["From"] = sender_email
    message["To"] = to_email

    text = f"""Hi there!

Please click the following link to verify your account:
{verification_link}
    """

    html = f"""
    <html>
        <body>
            <p>Hi there!<br><br>
            Please click the following link to verify your account:<br>
            <a href="{verification_link}">Verify my account</a>
            </p>
        </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP("smtp.maileroo.io", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, message.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", str(e))
