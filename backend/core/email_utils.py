import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def send_otp_email(to_email: str, code: str, purpose: str = "Password Reset"):
    sender_email = os.environ.get("SMTP_EMAIL")
    sender_password = os.environ.get("SMTP_PASSWORD")
    
    if not sender_email or not sender_password:
        raise HTTPException(status_code=500, detail="Server email configuration is missing.")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    
    if purpose == "Registration":
        msg['Subject'] = "LACBot - Account Verification Code"
        body = f"Welcome to LACBot!\n\nYour account verification code is: {code}\n\nThis code will expire in 15 minutes."
    else:
        msg['Subject'] = "LACBot - Password Reset Verification Code"
        body = f"Your password reset verification code is: {code}\n\nThis code will expire in 15 minutes."
        
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        logger.error(f"SMTP Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to send verification email.")