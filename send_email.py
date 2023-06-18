from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.text import MIMEText
import smtplib 
import os
import logging
import markdown



port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('MAIL_USERNAME')
PASSWORD = os.environ.get('MAIL_PASSWORD')

markdown.markdownFromFile(input='data.md', output='data.html')
dataset = open("data.html", 'r').read()
#  html = BeautifulSoup(data.md, 'html.parser')
# print(soup.get_text())


msg = MIMEMultipart()
part = MIMEBase('application', "octet-stream")
part.set_payload(open("data.html", "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="data.html"')
msg.attach(MIMEText("data.html", "html"))
msg.attach(part)

logging.info('username '+USERNAME)

server = smtplib.SMTP_SSL(smtp_server, port)
server.login(USERNAME,PASSWORD)
server.sendmail(
  "myrockemail@gmail.com", 
  "kubesonar@gmail.com", 
  dataset)
server.quit()

