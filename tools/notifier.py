import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import config
from utils.logger import get_logger

logger = get_logger(__name__)

def send_email(subject: str, body: str, is_html: bool = False):
    """
    Sends an email notification using SMTP.
    
    Args:
        subject (str): The email subject line.
        body (str): The email body content.
        is_html (bool): Whether the body is HTML formatted.
    """
    if not config.EMAIL_FROM or not config.EMAIL_PASSWORD or not config.EMAIL_TO:
        logger.warning("Email credentials not fully configured. Skipping notification.")
        return

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = config.EMAIL_FROM
    msg["To"] = config.EMAIL_TO
    
    if is_html:
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(config.EMAIL_FROM, config.EMAIL_PASSWORD)
            server.send_message(msg)
            logger.info(f"Successfully sent email notification to {config.EMAIL_TO}")
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
