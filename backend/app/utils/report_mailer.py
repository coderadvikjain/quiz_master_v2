from email.message import EmailMessage
import smtplib
import os
from app.config import Config

def send_report_email(to_email, subject, body, attachment_path=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = Config.MAIL_USERNAME
    msg["To"] = to_email
    msg.add_alternative(body, subtype="html")

    if attachment_path:
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(attachment_path))
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.send_message(msg)
            print(f"✅ Monthy Report Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send Monthy Report email to {to_email}: {e}")