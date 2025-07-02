#!/usr/bin/env python3

import os
import sys
import pwd
import spwd
import socket
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText

# Configuration
WARN_DAYS = 10
HOSTNAME = socket.gethostname()
SMTP_SERVER = ""
SMTP_PORT = 25
FROM_EMAIL = ""

# User to email mapping
USER_EMAIL_MAP = {
    "",
    "",
}

def send_notification(username, email, days_left, expiry_date):
    subject = f"Password Expiration Warning - {HOSTNAME}"
    
    body = f"""Your password on server '{HOSTNAME}' will expire in {days_left} days.

Account: {username}
Server: {HOSTNAME}
Expiration Date: {expiry_date.strftime('%Y-%m-%d')}

Please change your password before it expires to avoid account lockout.

To change your password, log in to {HOSTNAME} and run: passwd"""

    msg = MIMEText(body)
    msg['From'] = FROM_EMAIL
    msg['To'] = email
    msg['Subject'] = subject
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.send_message(msg)

def get_password_expiry_date(username):
    shadow_entry = spwd.getspnam(username)
    
    if shadow_entry.sp_max == -1:
        return None  # Password never expires
    
    last_change = shadow_entry.sp_lstchg
    max_days = shadow_entry.sp_max
    
    if last_change is None or last_change == -1:
        return None
    
    last_change_date = datetime(1970, 1, 1) + timedelta(days=last_change)
    expiry_date = last_change_date + timedelta(days=max_days)
    
    return expiry_date

def main():
    if os.geteuid() != 0:
        print("This script must be run as root")
        sys.exit(1)
    
    today = datetime.now().date()
    
    # Get regular users (UID >= 1000 and < 65534)
    users = [user.pw_name for user in pwd.getpwall() if 1000 <= user.pw_uid < 65534]
    
    for username in users:
        if username not in USER_EMAIL_MAP:
            continue
        
        expiry_date = get_password_expiry_date(username)
        
        if expiry_date is None:
            continue
        
        days_left = (expiry_date.date() - today).days
        
        if days_left <= WARN_DAYS:
            email = USER_EMAIL_MAP[username]
            send_notification(username, email, days_left, expiry_date)

if __name__ == "__main__":
    main()