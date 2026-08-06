import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration
sender_email = "your.soc.dot@gmail.com"
sender_password = "jmwz tayi xtap zngs"

receiver_email = "rahmanmeen206@gmail.com"

failures = {}
alerted = set()
def send_email_alert(ip, count):
    subject = "⚠ Security Alert: Brute Force Detected"
    body = f"""
Brute force attack detected!z

IP Address: {ip}
Failed Attempts: {count}
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"[EMAIL SENT] Alert sent for IP {ip}")
    except Exception as e:
        print(f"[ERROR] Could not send email: {e}")

with open("auth_large.log", "r") as f:
    for line in f:
        if "Failed password" in line:
            match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
            if match:
                ip = match.group(1)
                failures[ip] = failures.get(ip, 0) + 1

                if failures[ip] >= 5 and ip not in alerted:
                    print(f"[ALERT] {ip} has {failures[ip]} failures!")
                    send_email_alert(ip, failures[ip])
                    alerted.add(ip)
                    alerted.add(ip)

