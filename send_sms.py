# -- coding: utf-8 --
import twilio
from twilio.rest import TwilioRestClient

try:

    account_sid = "AC21495bf375be89be5abd4d11b93ac569"
    auth_token = "2b2d8fd1597ebd74e62a85a9b25e2c55"
    client = TwilioRestClient(account_sid, auth_token)
    text = 'Picture messaging status:'
    URL= 'https://dl.dropboxusercontent.com/u/11489766/twilio/elearning/success.jpg'
    message = client.messages.create(body=text, 
                                     to="+14156138051",
                                     from_="+14157924413", 
                                     MediaUrl=URL)
    print message.sid
except twilio.TwilioRestException as e:
  print e

