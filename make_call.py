# -- coding: utf-8 --
import twilio
from twilio.rest import TwilioRestClient

try:

    account_sid = "AC21495bf375be89be5abd4d11b93ac569"
    auth_token = "2b2d8fd1597ebd74e62a85a9b25e2c55"
    client = TwilioRestClient(account_sid, auth_token)
    text = 'Picture messaging status:'
    URL= 'http://d18eeb7b.ngrok.io/hello'
    call = client.calls.create(body=text, 
                                     to="+14156138051",
                                     from_="+14157924413", 
                                     url=URL)
    print call.sid
except twilio.TwilioRestException as e:
  print e

