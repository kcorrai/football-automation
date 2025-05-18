import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_email_config(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config["smtp_server"], config["smtp_port"], config["email_username"], config["email_password"]

def send_email(smtp_server, smtp_port, username, password, recipient, subject, body):
    """
    Sends an email.
    """
    msg = MIMEMultipart()
    msg['From'] = f"Kcorrai Football Data"
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

def send_email_now(config_path):
    """
    Sends an email immediately using configuration from the config file.
    """
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    smtp_server = config["smtp_server"]
    smtp_port = config["smtp_port"]
    username = config["email_username"]
    password = config["email_password"]
    recipient = config["recipient_email"]
    subject = config["email_subject"]
    body = "daily football matches"

    # Correctly call send_email with updated sender name
    send_email(smtp_server, smtp_port, username, password, recipient, subject, body)