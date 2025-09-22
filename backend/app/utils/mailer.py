import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import Config

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = Config.MAIL_USERNAME
    msg["To"] = to_email

    msg.attach(MIMEText(body, "html", "utf-8"))

    try:
        with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.sendmail(Config.MAIL_USERNAME, to_email, msg.as_string().encode("utf-8"))
            print(f"✅ Reminder Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send Reminder email to {to_email}: {e}")