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
    if 'camera' in t.text:
        print("Camera message received!")
        api.messages.create(roomId=room_id, text ="Let me find that camera stream")
        url = getCamera()
        api.messages.create(roomId=room_id, text=url)
    elif 'source' in t.text:
        print("Request for source code!")
        api.messages.create(roomId=room_id, text="My source code can be found at \n https://github.com/shaurobi/sparkbotlambda")
    elif 'help' in t.text:
        print("Request for Help!")
        api.messages.create(roomId=room_id, text="Ask for a camera feed, or my source code!")
    else:
        response = 'NO COMMAND MATCH FOUND: ' + t.text
        api.messages.create(roomId=room_id, text=response)
    return "Finished"
