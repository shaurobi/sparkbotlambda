import json
import os
from webexteamssdk import WebexTeamsAPI
import requests

api = WebexTeamsAPI()

# the lambda handler function
def getCamera():
    url = "http://api.meraki.com/api/v0/networks/L_602356450160820134/cameras/Q2HV-B63K-AAHS/videoLink"
    headers = {
        'x-cisco-meraki-api-key': os.environ['MERAKI_DASHBOARD_KEY'],
        'cache-control': "no-cache"
        }
    result = requests.request("GET", url, headers=headers)
    response = result.json()
    return response['url']

def messageHandler(inc_message):
    inc_message=inc_message.lower()
    if 'batman' in inc_message or 'whoareyou' in inc_message:
        msg = "I'm Batman!"
        msgtype = "text"
    elif 'help' in inc_message:
        msg = ("""Hi! I'm a **Lambda Proof of Concept Bot**. Here's a list of things you can do -
    Ask for the CHLORINE level to see what the tanks doing.
    You can also ask WHO is on duty and START a Webex meeting if needed.
    You can also request to view my SOURCE CODE
    I can tell you a DADJOKE .""")
        msgtype = "markdown"

    elif 'who' in inc_message:
        msg = 'Current supervisor on duty is Roger Greene (roggreen@cisco.com)'
        msgtype = "text"

    elif 'cash me outside' in inc_message:
        msg = 'HOW BOUH DAT'
        msgtype = 'text'

    elif 'test' in inc_message:
        msg = 'Message received loud and clear! thanks <@personEmail:' + person + '>'
        msgtype = "markdown"

    elif 'start' in inc_message:
        msg = 'Click on the below link to start a Webex! \r\n http://cs.co/shaun'
        msgtype = 'markdown'

    elif 'source code' in inc_message:
        msg = """You can view my source code at this link:
       https://github.com/shaurobi/sparkbotlambda"""
        msgtype = "text"

    elif 'chlorine' in inc_message:
        chlorine = random.randrange(0, 100)
        msgtype = "text"
        if chlorine > 80:
            msg = "Alert! Chlorine is dangerously high at " + str(chlorine) + "%"
        else:
            msg = "Chlorine currently at " + str(chlorine) + "%"

    elif 'beer' in inc_message:
        msg = "beer"
        doc = "http://employees.org/~shaurobi/beer1.jpg"

    elif 'roomid' in inc_message:
        msg1 = "RoomID for this room is " + webhook['data']['roomId']
        msg= str(msg1)
        msgtype = "text"

    elif 'members' in inc_message:
        peopleCount = random.randrange(100,10000)
        msgtype = "text"
        msg = "There are currently " + str(peopleCount) + " people in the Member's Section"

    elif 'southern' in inc_message:
        peopleCount = random.randrange(1000,20000)
        msgtype = "text"
        msg = "There are currently " + str(peopleCount) + " people in the Southern Stand"

    elif 'dadjoke' in inc_message:
        msg = getDadJoke()
        msgtype = "text"
    else:
        msg = "NO COMMAND MATCH FOUND:"+inc_message
        msgtype="text"
    
    return msg, msgtype
    
    
    
    
def getDadJoke():
    """
    Gets a random Dad joke and returns it as a string
    :return joke: string
    """
    header1 ={ "Accept":"application/json"}
    uri = "https://icanhazdadjoke.com/"
    joke = requests.get(uri, headers=header1)
    joke = joke.json()
    return str(joke['joke'])


def lambda_handler(event, context):
    print(event['body'].__class__)
    print(event['body'])
    message = json.loads(event['body'])
    me = api.people.me()
    if message['actorId'] == me.id:
        print("Ignoring event due to actorId = me")
        return 0
    # assign the WebexTeams message id to a variable
    msg_id = message['data']['id']
    # assign the WebexTeams roomId to a variable (for the Bot to respond into the right room dynamically)
    room_id = message['data']['roomId']
    
    t = api.messages.get(msg_id)
    print(t.text)
    msg, msgtype = messageHandler(t.text)
    print(msg, msgtype)
    api.messages.create(roomId=room_id, text=msg)
    return "Finished"
