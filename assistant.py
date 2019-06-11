from slack import RTMClient, WebClient
import requests
import re
import json
from attachments import available_features
from config.config import bot_token,CHATBOT_API
from config import errors

rtmclient = RTMClient(token=bot_token)
sclient = WebClient(bot_token)


# Call chatbot only when mentioned
def direct_mention(message_text: str) -> (str, str):
    info = re.search("^<@(|[WU].+?)>(.*)", message_text)
    if info:
        return info.group(1), info.group(2).strip()
    else:
        return None, None

def list_apps(response):
    res = ""
    for i in range(len(response)):
        res+= "*App name:* " + response["apps"][i]["name"] + "\n*id:* " + response["apps"][i]["id"] +"\n*Description:* " + response["apps"][i]["description"] + "\n*Github:* " + response["apps"][i]["github_url"] +"\n\n"
    return res

def process_message(**data):
    channel_id = data['data']['channel']
    user_id, message_text = direct_mention(data['data']['text'])

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
                        attachments=available_features.available_features(response),
                    )
                else:
                    sclient.chat_postMessage(
                        channel=channel_id,
                        text=response["text"],
                    )
            except:
                sclient.chat_postMessage(
                        channel=channel_id,
                        text=list_apps(response)
                    )

        except ConnectionRefusedError:
            return errors.CONNECTION_ERR



if __name__ == "__main__":
    # Unique id given to bot for the particular workspace
    bot_id = sclient.api_call("auth.test")["user_id"]
    # Connect with rtm api and check for new messages
    rtmclient.on(event='message', callback=process_message)
    rtmclient.start()
