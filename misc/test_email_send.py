from src.utils.sendgrid_mailer import Sendgrid_Mailer as Mailer
import sys

recipient1 = "wangjia.sun@gmail.com"

args = len (sys.argv)

if args < 2:
    print ('Please provide Sendgrid API key')
    sendgrid_api_key = input ('Enter your application key :')
    print ('Thanks for the input provided')
else:
    sendgrid_api_key = sys.argv [1]

mailer = Mailer(sendgrid_api_key)
mailer.send_email (recipient1, 'subject', 'str (content)')
