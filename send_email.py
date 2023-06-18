from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import smtplib 
import os


port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('MAIL_USERNAME')
PASSWORD = os.environ.get('MAIL_PASSWORD')

msg = MIMEMultipart()
part = MIMEBase('application', "octet-stream")
part.set_payload(open("file://data.md", "rb").read())
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="file://data.md"')
msg.attach(part)

server = smtplib.SMTP_SSL(smtp_server, port)
server.login("myrockemail@gmail.com","pvbrhwpdcikrvale")
server.sendmail(
  "myrockemail@gmail.com", 
  "kubesonar@gmail.com", 
  msg.as_string())
server.quit()