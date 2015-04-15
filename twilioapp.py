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
      Press any other key to start over....
      """
    response = twiml.Response()

    with response.gather(numDigits=1, action="/handle-key", method="POST",finishOnKey='*',timeout='15') as g:
     g.say(MenuString)
    return Response(str(response), mimetype='text/xml')


@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""

    digit_pressed = request.values.get('Digits', None)

    if digit_pressed == "1":
                resp = twiml.Response()
                resp.say("Just Texted you a link to the Rezuhmay:")
                resp.sms("https://dl.dropboxusercontent.com/s/xv3071vwfdh4dvu/Kaveh%20Mehrjoo_3_24_15.pdf?dl=0")
                return str(resp)
    elif digit_pressed == "2":
                resp = twiml.Response()
                resp.say("Just Texted you a link to Linkin Profile:")
                resp.sms("https://www.linkedin.com/pub/kaveh-mehrjoo/4/194/588")
                resp.hangup()
                return str(resp)
    elif digit_pressed == "3":
                resp = twiml.Response()
                resp.say("Just Texted you a link to Master Thesis")
                resp.sms("http://scholar.lib.vt.edu/theses/available/etd-09202007-013736/unrestricted/kaveh_thesis_v2.pdf")
                resp.hangup()
                return str(resp)
    elif digit_pressed == "4":
                resp = twiml.Response()
                resp.say("Just Texted you a link to the Blog")
                resp.sms("http://community.arubanetworks.com/t5/Technology-Blog/Watch-Advanced-quot-How-To-quot-Videos-on-Configuring-ClearPass/ba-p/41420")
                resp.hangup()
                return str(resp)
    elif digit_pressed == "5":
                resp = twiml.Response()
                resp.say("Just sent you a picture of Mee-ka the Dog")
                resp.sms("https://dl.dropboxusercontent.com/u/22879346/Mika.jpg")
                #resp.hangup()
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
        resp = twiml.Response()
        resp.say("Didn't recognize your selection. Let's try again...")
        return redirect('/voice')

@app.route('/sms')
def sms():
    MenuString=""" Hello, thank you for considering Kaveh for Twilio. 
To learn more, please indicate your selection by texting its number.
      1. Resume 
      2. LinkedIn Profile
      3. Master's Thesis
      4. Blog Post
      5. Something Cool
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