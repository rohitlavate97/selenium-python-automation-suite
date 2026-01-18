import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class EmailUtil:

    @staticmethod
    def send_email(subject, body, sender, password, recipients, attachments=None):
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = ",".join(recipients)
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        if attachments:
            for file in attachments:
                if os.path.exists(file):
                    part = MIMEBase("application", "octet-stream")
                    with open(file, "rb") as f:
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file)}")
                    msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# class EmailUtil:
#
#     @staticmethod
#     def send_email(subject, body, sender, password, recipients):
#         msg = MIMEMultipart()
#         msg["From"] = sender
#         msg["To"] = ",".join(recipients)
#         msg["Subject"] = subject
#
#         msg.attach(MIMEText(body, "html"))
#
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(sender, password)
#         server.send_message(msg)
#         server.quit()
