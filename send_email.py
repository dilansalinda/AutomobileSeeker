import smtplib 
import os


port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('MAIL_PASSWORD')
PASSWORD = os.environ.get('MAIL_PASSWORD')


server = smtplib.SMTP_SSL(smtp_server, 465)
server.login(USERNAME,PASSWORD)
server.sendmail(
  USERNAME, 
  "kubesonar@gmail.com", 
  "this message is from python")
server.quit()
