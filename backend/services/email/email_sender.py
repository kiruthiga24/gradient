import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.logger import logger

SMTP_SERVER = "smtp.gmail.com"  # e.g., smtp.gmail.com
SMTP_PORT = 587
SMTP_USER = "sunil@saturam.com"
SMTP_PASSWORD = "laqj aype qncw sxxx" # my gmail appcode as it pass 2f, generate code from https://myaccount.google.com/apppasswords

def send_email(from_email, to_email, subject, body_text):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body_text, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        logger.info(f"Email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False
