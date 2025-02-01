import smtplib
import os
import schedule
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date

# Gmail credentials
GMAIL_USER = "ricky.email.bot@gmail.com"
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
TO_EMAILS = ["rickylin543@gmail.com", "ricky.lin1@motorolasolutions.com"]
SUBJECT = "GO AND DO YOUR TIMESHEET"
BODY = """
<p>Don't forget about your timesheets, buddy! ⏳</p>
<p><a href="https://workforcenow.adp.com/theme/index.html#/Myself/MyselfTabTimecardsAttendanceSchCategoryTLMWebMyTimecard" target="_blank">Click here to submit your timesheet</a></p>
"""
LAST_SENT_DATE = None
def send_email():
    global LAST_SENT_DATE
    today = date.today()

    # Only send email if 14 days have passed since the last email
    if LAST_SENT_DATE is None or (today - LAST_SENT_DATE).days >= 13:
        try:
            # Set up email
            msg = MIMEMultipart()
            msg["From"] = GMAIL_USER
            msg["To"] = ", ".join(TO_EMAILS)  # ✅ Set all recipients at once
            msg["Subject"] = SUBJECT
            msg.attach(MIMEText(BODY, "html"))

            # Connect to Gmail SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)

            # Send email once to all recipients
            server.sendmail(GMAIL_USER, TO_EMAILS, msg.as_string())
            print(f"✅ Email sent successfully to {', '.join(TO_EMAILS)} on {today}")

            # Close server
            server.quit()
            
            # Update last sent date
            LAST_SENT_DATE = today  

        except Exception as e:
            print(f"❌ Error: {e}")

# Schedule to check every Friday at 10 AM
schedule.every().friday.at("10:00").do(send_email)

send_email()
# Schedule the email every Friday at 10 AM
schedule.every().friday.at("10:00").do(send_email)

print("📅 Scheduler started! Waiting for the next scheduled email...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
