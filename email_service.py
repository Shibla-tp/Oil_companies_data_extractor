import csv
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import time

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_emails_from_csv(csv_file):
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            to_email = row.get("Email")
            brand = row.get("Brand", "there")

            if not to_email:
                continue

            subject = "Potential Collaboration Opportunity"
            body = f"""Dear Team,

Greetings from GEW LLC.

We are reaching out to explore a potential collaboration with {brand}. GEW LLC works with organizations across the oil and energy sector, supporting strategic partnerships and regional business initiatives.

We would be glad to connect and discuss this further if of interest.

Kind regards,
GEW LLC
"""

            msg = MIMEMultipart()
            msg["From"] = EMAIL_USER
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(EMAIL_USER, EMAIL_PASS)
                    server.send_message(msg)

                print(f"✅ Email sent to {to_email}")
                time.sleep(2)

            except Exception as e:
                print(f"❌ Failed for {to_email}: {e}")

