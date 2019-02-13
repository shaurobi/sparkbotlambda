import json
import os
from webexteamssdk import WebexTeamsAPI
import requests



api = WebexTeamsAPI()

# the lambda handler function
def lambda_handler(event, context):
    """Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.
    """
    # print the event details received from the Spark Webhook for logging
    print("Received event: " + json.dumps(event, indent=2))
    #check if self generated this event
    print(event['body'].__class__)
    print(event['body'])
    message = json.loads(event['body'])
    me = api.people.me()
    if message['actorId'] == me.id:
        print("Ignoring event due to actorId = me")
        return 0
    # assign the Spark message id to a variable
    msg_id = message['data']['id']
    # assign the Spark roomId to a variable (for the Bot to respond into the right room dynamically)
    room_id = message['data']['roomId']
    
    t = api.messages.get(msg_id)
    t = t.lower()
    if t.text:
        if 'camera' in t:
            url = "http://api.meraki.com/api/v0/networks/L_602356450160820134/cameras/Q2HV-B63K-AAHS/videoLink"
            headers = {
                'x-cisco-meraki-api-key': os.environ['MERAKI_DASHBOARD_KEY'],
                'cache-control': "no-cache"
                }
            response = requests.request("GET", url, headers=headers)
        print(response.text)	
        else:
        response = 'NO COMMAND MATCH FOUND: ' + t.text
        api.messages.create(roomId=room_id, text=response)
    else:
        print("Error: No Text Received in msg")
    return "Finished"
