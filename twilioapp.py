Last login: Sun Apr 19 15:33:07 on ttys000
SJC-KAVEH-MB-2:~ kaveh$ ssh kaveh@10.1.40.244
kaveh@10.1.40.244's password: 
Welcome to Ubuntu 14.10 (GNU/Linux 3.16.0-23-generic x86_64)

 * Documentation:  https://help.ubuntu.com/

  System information as of Sun Apr 19 15:33:49 PDT 2015

  System load:  0.0               Processes:           107
  Usage of /:   1.6% of 97.32GB   Users logged in:     1
  Memory usage: 27%               IP address for eth0: 10.1.40.244
  Swap usage:   0%

  Graph this data and manage this system at:
    https://landscape.canonical.com/

96 packages can be updated.
62 updates are security updates.

Last login: Sun Apr 19 13:07:50 2015 from 10.1.40.243
kaveh@ubuntu:~$ git config --global user.name kmehrjoo
kaveh@ubuntu:~$ pwd
/home/kaveh
kaveh@ubuntu:~$ git config --global user.email kaveh.air@gmail.com
kaveh@ubuntu:~$ git ?
git: '?' is not a git command. See 'git --help'.

Did you mean one of these?
	am
	gc
	mv
	rm
kaveh@ubuntu:~$ cd twi
-bash: cd: twi: No such file or directory
kaveh@ubuntu:~$ pwd
/home/kaveh
kaveh@ubuntu:~$ cd /twilio/
kaveh@ubuntu:/twilio$ ls
ngrok  starter-python-master  starter-python-master.zip
kaveh@ubuntu:/twilio$ cd starter-python-master/
kaveh@ubuntu:/twilio/starter-python-master$ ls
app.py	app.py.4.14.ubuntu.1  LICENSE  README.md  static  templates
kaveh@ubuntu:/twilio/starter-python-master$ vi app.py

import os

from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from twilio import twiml
from twilio.rest import TwilioRestClient

# Pull in configuration from system environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

# create an authenticated client that can make requests to Twilio for your
# account.
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Create a Flask web app
app = Flask(__name__)

# Render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Handle a POST request to send a text message. This is called via ajax
# on our web page
@app.route('/message', methods=['POST'])
def message():
    # Send a text message to the number provided
    message = client.sms.messages.create(to=request.form['to'],
                                         from_=TWILIO_NUMBER,
                                         body='Have fun with your Twilio development!')

    # Return a message indicating the text message is enroute
    return 'Message on the way!'

# Handle a POST request to make an outbound call. This is called via ajax
# on our web page
@app.route('/call', methods=['POST'])
def call():
    # Make an outbound call to the provided number from your Twilio number
    call = client.calls.create(to=request.form['to'], from_=TWILIO_NUMBER,
                               url='http://twilio-elearning.herokuapp.com/starter/voice.php')

    # Return a message indicating the call is coming
    return 'Call inbound!'

# Generate TwiML instructions for an outbound call
@app.route('/hello', methods = ['POST'])
def hello():
    response = twiml.Response()
    response.say('You just made your first Twilio Voice Call', voice='woman')
    response.play('http://demo.twilio.com/docs/classic.mp3')
    response.hangup()
    return Response(str(response), mimetype='text/xml')

@app.route('/voice', methods = ['POST','GET'])
def voice():

    MenuString=""" Hello, Thank you for considering me for Twilio: 
      For a Link to 
      Rezuhmay, press 1 
      ....................................
      Linkdin Profile, Press 2....
      .......................................
      Master's Thesis, Press 3....
      .....................................
      Technical Videos, Press 4 ....
      ........................................
      Cool Picture of the Dog, Press 5 ...
      ......................................
      To talk to the Man, Press 6...
      ......................................
      To Hang Up, Press 8 ...............
      .....................................
      Press any other key to start over....
      """
    response = twiml.Response()

    with response.gather(numDigits=1, action="/handle-key", method="POST",finishOnKey='*',timeout='15') as g:
     g.say(MenuString)

    return str(response)


@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""

    digit_pressed = request.values.get('Digits', None)

    if digit_pressed == "1":
                resp = twiml.Response()
                resp.say("Just Texted you a link to the Rezuhmay:")
                resp.sms("https://dl.dropboxusercontent.com/s/xv3071vwfdh4dvu/Kaveh%20Mehrjoo_3_24_15.pdf?dl=0")
                resp.say("Returning to the main menu")
                resp.redirect('/voice')
                return str(resp)
    elif digit_pressed == "2":
                resp = twiml.Response()
                resp.say("Just Texted you a link to Linkin Profile:")
                resp.sms("https://www.linkedin.com/pub/kaveh-mehrjoo/4/194/588")
                resp.say("Returning to the main menu")
                resp.redirect('/voice')
                return str(resp)
    elif digit_pressed == "3":
                resp = twiml.Response()
                resp.say("Just Texted you a link to Master Thesis")
                resp.sms("http://scholar.lib.vt.edu/theses/available/etd-09202007-013736/unrestricted/kaveh_thesis_v2.pdf")
                resp.say("Returning to the main menu")
                resp.redirect('/voice')
                return str(resp)
    elif digit_pressed == "4":
                resp = twiml.Response()
                resp.say("Just Texted you a link to the Blog")
                resp.sms("http://community.arubanetworks.com/t5/Technology-Blog/Watch-Advanced-quot-How-To-quot-Videos-on-Configuring-ClearPass/ba-p/41420")
                resp.say("Returning to the main menu")
                resp.redirect('/voice')
                return str(resp)
    elif digit_pressed == "5":
                resp = twiml.Response()
                resp.say("Just sent you a picture of Mee-ka the Dog")
                resp.sms("https://dl.dropboxusercontent.com/u/22879346/Mika.jpg")
                resp.say("Returning to the main menu")
                resp.redirect('/voice')
                return str(resp)
    elif digit_pressed == "6":
                resp = twiml.Response()
                resp.say("Calling the Man")
                resp.dial("+14156138051")
                return str(resp)
    # If the caller pressed anything but 1, redirect them to the homepage.
    elif digit_pressed == "8":
                resp = twiml.Response()
                resp.say("Thanks for calling ... Hope to meet you soon in person")
                resp.hangup()
                return str(resp)
    else:
        print "here"
        resp = twiml.Response()
        resp.say("Let's try again...")
        resp.redirect('/voice')
        return str(resp)

@app.route('/sms')
def sms():
    MenuString=""" Hello, thank you for considering Kaveh for Twilio. 
To learn more, please indicate your selection by texting its number.
      1. Resume 
      2. LinkedIn Profile
      3. Master's Thesis
      4. Blog Post
      5. Meet Mika
      6. Call Kaveh
      """
    r = twiml.Response()
    body = request.values.get('Body',None)
    print body
    if body == "1":
       r.message("https://dl.dropboxusercontent.com/s/xv3071vwfdh4dvu/Kaveh%20Mehrjoo_3_24_15.pdf?dl=0")
    elif body == "2":
       r.message("https://www.linkedin.com/pub/kaveh-mehrjoo/4/194/588")
    elif body == "3" :
       r.message("http://scholar.lib.vt.edu/theses/available/etd-09202007-013736/unrestricted/kaveh_thesis_v2.pdf")
    elif body == "4" :
       r.message("http://community.arubanetworks.com/t5/Technology-Blog/Watch-Advanced-quot-How-To-quot-Videos-on-Configuring-ClearPass/ba-p/41420")
    elif body == "5" :
           with r.message("Meet Mika the dog") as m:
               m.media("https://dl.dropboxusercontent.com/u/22879346/Mika.jpg")
    elif body == "6" :
           r.message("14156138051")
    else :
       r.message(MenuString)
    return Response(str(r), mimetype='text/xml')


if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)
                                                                                    
