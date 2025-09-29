import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtp_config import smtp


sender_email = smtp['sender_email']
app_password = smtp['app_password']

def send_email(receivers, subject, body_html, body_text=""):
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    
    if isinstance(receivers, list):
        msg["To"] = ", ".join(receivers)
    else:
        msg["To"] = receivers

    msg["Subject"] = subject

    if body_text:
        msg.attach(MIMEText(body_text, "plain"))
    msg.attach(MIMEText(body_html, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)

        server.sendmail(sender_email, receivers, msg.as_string())
        server.quit()
        print("🌵 Gửi email thành công!")
    except Exception as e:
        pass