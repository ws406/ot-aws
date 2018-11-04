import sendgrid
import os
from sendgrid.helpers.mail import *

class Sendgrid_Mailer:
    # Your email details
    api_key = "odds.tracker.2018@gmail.com"

    def __init__ (self, sendgrid_api_key):
        self.sendgrid = sendgrid.SendGridAPIClient(sendgrid_api_key)
        # sg = sendgrid.SendGridAPIClient (apikey = os.environ.get ('SENDGRID_API_KEY'))

    def send_email (self, to_addr, subject, content):
        # using SendGrid's Python Library
        # https://github.com/sendgrid/sendgrid-python

        from_email = Email ("odds.tracker.2018@gmail.com")
        to_email = Email (to_addr)
        content = Content ("text/plain", content)
        mail = Mail (from_email, subject, to_email, content)
        response = self.sendgrid.client.mail.send.post (request_body = mail.get ())
        # print (response.status_code)
        # print (response.body)
        # print (response.headers)
        print ("Email sent to '" + to_addr + "' successfully!")
