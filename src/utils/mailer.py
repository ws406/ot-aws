# Send emails in Python, converted for Python 3.6 by iCrazyBlaze
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:
	# Your email details
	fromaddr = "odds.tracker.2018@gmail.com"
	PASSWORD = "OddsTracker123!"

	def __init__(self):
		pass
	
	def send_email(self, to_addr, subject, content):
		# try:
		msg = MIMEMultipart()
		msg['From'] = self.fromaddr
		msg['To'] = to_addr
		msg['Subject'] = subject
	
		msg.attach(MIMEText(content, 'plain'))
	
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(self.fromaddr, self.PASSWORD)
		text = msg.as_string()
		server.sendmail(self.fromaddr, to_addr, text)
		server.quit()
		print("Email sent to '" + to_addr + "' successfully!")
		# except:
		# 	print("An error occured!")