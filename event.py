import re
import requests
from config.panic import *
from config.config import CHATBOT_API , SlackMessage
from slackResponse import create_slack_response
import json


# Separate message text from mention
def direct_mention(message_text: str) -> (str, str):
    info = re.search("^<@(|[WU].+?)>(.*)", message_text)
    if info:
        return info.group(1), info.group(2).strip()
    else:
        return None, None


# Send text to watson api through chatbot api
def call_chatbot_api(message_text, user):
    try:
        response = requests.post(url=CHATBOT_API, json={'text': message_text, 'user':"SLACK_"+user})
        return create_slack_response(json.loads(response.json()))
    except Exception as e:
        raise_exception("Error querying API", str(e))


# Handle different event types and connection errors
def _event_handler(event_type: str, slack_event: json):
    resp = SlackMessage
    if event_type == "app_mention":
        bot_id, message_text = direct_mention(slack_event['event']['text'])
        resp.channel= slack_event['event']['channel']
        resp.user = slack_event['event']['user']

    elif event_type == "interactive_message":
        message_text = slack_event['actions'][0]["value"]
        resp.channel = slack_event['channel']['id']
        resp.user = slack_event['user']['id']

    else:
        raise_exception("Error while handling event", "Invalid Event")

    call_chatbot_api(message_text, resp.user)

    return json.dumps("Sure!")
