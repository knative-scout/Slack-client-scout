from slack import WebClient
from flask import Flask, request, make_response
from config import errors
from config.config import bot_token, CHATBOT_API,verify_token
import json
import requests
import re
from attachments import available_features

slack = WebClient(bot_token)
app = Flask(__name__)

def verify_slack_token(request_token):
    if verify_token != request_token:

        print("Error: invalid verification token!")
        print("Received {} but was expecting {}".format(request_token, verify_token))

    return make_response("Request contains invalid Slack verification token", 403)

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

def send_messages_to_watson(message):
    try:
        response = requests.post(url=CHATBOT_API, json={'text': message})

    except ConnectionError:
        errors.CONNECTION_ERR



def _event_handler(event_type, slack_event):


    if event_type == "app_mention":
        bot_id, message_text = direct_mention(slack_event['event']['text'])
        channel_id = slack_event['event']['channel']

    elif event_type == "interactive_message":
        message_text = slack_event['actions'][0]["selected_options"][0]["value"]
        channel_id = slack_event['channel']['id']

    else:
        return make_response("Invalid message", 403, )

    try:

        response = requests.post(url=CHATBOT_API, json={'text': message_text})

        print("watson", response.text)
        try:
            response = json.loads(response.text)

            if 'options' in response:
                slack.chat_postMessage(
                    channel=channel_id,
                    attachments=[available_features.available_features(response)],
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



@app.route("/listening", methods=["GET", "POST"])
def incoming_messages():
    # Parse the request payload
    try:
        form_json = json.loads(request.form["payload"])
        verify_slack_token(form_json["token"])
        print(form_json)
        return _event_handler(form_json['type'],form_json)
    except:

        slack_event = request.get_json()
        print("This is slack", slack_event)
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
