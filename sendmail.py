import smtplib
from email.message import EmailMessage
from config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT

def send_email(to_email, subject, body):
    # Create the email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = MAIL_USERNAME
    msg['To'] = to_email
    msg.set_content(body)

    # Connect to SMTP server and send email
    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        server.starttls()  # Upgrade the connection to secure
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.send_message(msg)
