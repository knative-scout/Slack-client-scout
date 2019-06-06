import os
from slack import RTMClient, WebClient
import requests
import re
import json
import attachments
from config import bot_token,CHATBOT_API
import errors

rtmclient = RTMClient(token=bot_token)
sclient = WebClient(bot_token)


# Call chatbot only when mentioned
def direct_mention(message_text: str) -> (str, str):
    info = re.search("^<@(|[WU].+?)>(.*)", message_text)
    if info:
        return info.group(1), info.group(2).strip()
    else:
        return None, None


def process_message(**data):
    channel_id = data['data']['channel']
    user_id, message_text = direct_mention(data['data']['text'])
    print(user_id, bot_id, data['data']['text'])

    if (user_id == bot_id):

        try:
            # Send user message to watson
            response = requests.post(url=CHATBOT_API, json={'text': message_text})

            try:
                response = json.loads(response.text)

                # Check for options in response
                if 'options' in response:
                    sclient.chat_postMessage(
                        channel=channel_id,
                        attachments=attachments.available_features(response),
                    )
                else:
                    sclient.chat_postMessage(
                        channel=channel_id,
                        text=response["text"],
                    )
            except:

                sclient.chat_postMessage(
                    channel=channel_id,
                    text=response["apps"][0]["name"],
                )
        except ConnectionRefusedError:
            return errors.CONNECTION_ERR


if __name__ == "__main__":
    # Unique id given to bot for the particular workspace
    bot_id = sclient.api_call("auth.test")["user_id"]

    # Connect with rtm api and check for new messages
    rtmclient.on(event='message', callback=process_message)
    rtmclient.start()
