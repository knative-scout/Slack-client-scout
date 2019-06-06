import os
from slack import RTMClient,WebClient
import requests
import re
import json
import attachments

tok= os.environ['BOTUSER_TOKEN']
rtmclient = RTMClient(token=tok)
sclient = WebClient(tok)

# Call chatbot only when mentioned
def direct_mention(message_text):

    info = re.search("^<@(|[WU].+?)>(.*)", message_text)
    if info:
        return (info.group(1), info.group(2).strip())
    else:
        (None, None)


def process_message(**data):
    channel_id = data['data']['channel']
    thread_ts = data['data']['ts']

    user_id, message_text =direct_mention(data['data']['text'])


    if(user_id == bot_id):

        # Send user message to watson
        response = requests.post(url="http://localhost:5000/messages",  json={'text': message_text})
        response = json.loads(response.text)

        # Check for options in response
        if('options' in response):
              sclient.chat_postMessage(
                channel=channel_id,
                attachments =attachments.available_features(response),
            )
        else:
            sclient.chat_postMessage(
                    channel=channel_id,
                    text=response["text"],
                )


if __name__ == "__main__":
    # Unique id given to bot for the particular workspace
    bot_id = sclient.api_call("auth.test")["user_id"]

    # Connect with rtm api and check for new messages
    rtmclient.on(event='message', callback=process_message)
    rtmclient.start()

# TODO: Error Handling
# TODO: Deploy script