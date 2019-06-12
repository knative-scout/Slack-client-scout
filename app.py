from slack import WebClient
from flask import Flask, request, make_response
from config import errors
from config.config import bot_token, CHATBOT_API
import json
import requests
import re
import attachments

slack = WebClient(bot_token)
app = Flask(__name__)

# Call chatbot only when mentioned
def direct_mention(message_text: str) -> (str, str):
    info = re.search("^<@(|[WU].+?)>(.*)", message_text)
    if info:
        return info.group(1), info.group(2).strip()
    else:
        return None, None

def list_apps(response):
    res = ""
    for i in range(len(response['apps'])):
        res+= "*App name:* " + response["apps"][i]["name"] + "\n*id:* " + response["apps"][i]["id"] +"\n*Description:* " + response["apps"][i]["description"] + "\n*Github:* " + response["apps"][i]["github_url"] +"\n\n"
    return res

def _event_handler(event_type, slack_event):

    if event_type == "app_mention":
        bot_id, message_text = direct_mention(slack_event['event']['text'])
        channel_id = slack_event['event']['channel']
        try:
            # Send user message to watson


            response = requests.post(url=CHATBOT_API, json={'text': message_text})
            print(response.text)
            try:
                response = json.loads(response.text)
                # texts = json.load(texts.text)

                # Check for options in response
                if 'options' in response:
                    slack.chat_postMessage(
                        channel=channel_id,
                        attachments=attachments.available_features.available_features(response),
                    )
                else:
                    slack.chat_postMessage(
                        channel=channel_id,
                        text=list_apps(response) + "\n" + response["text"]
                    )

            except:
                slack.chat_postMessage(
                    channel=channel_id,
                    text=response["text"],
                )

        except ConnectionRefusedError:
            return errors.CONNECTION_ERR

        print(slack_event)
        return make_response("Welcome Message Sent", 200, )


@app.route("/listening", methods=["GET", "POST"])
def incoming_messages():
    slack_event = request.get_json()
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route('/health', methods=['GET', 'POST'])
def health_check():
    status = {"ok": True}
    return make_response(json.dumps(status), 200,)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
