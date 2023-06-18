import smtplib 
import os


port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('MAIL_USERNAME')
PASSWORD = os.environ.get('MAIL_PASSWORD')

print(USERNAME)
print(PASSWORD)

server = smtplib.SMTP_SSL(smtp_server, port)
server.login(USERNAME,PASSWORD)
server.sendmail(
  USERNAME, 
  "kubesonar@gmail.com", 
  "this message is from python")
server.quit()
