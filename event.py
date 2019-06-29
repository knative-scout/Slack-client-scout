import re
import requests
from flask import make_response
from config.panic import *
from config.config import CHATBOT_API
from slackResponse import convert_watson_to_slack
import json


# Separate message text from mention
def direct_mention(message_text: str) -> (str, str):
    info = re.search("^<@(|[WU].+?)>(.*)", message_text)
    if info:
        return info.group(1), info.group(2).strip()
    else:
        return None, None


# Send text to watson api through chatbot api
def connect_to_watson(message_text, channel_id,user):
    try:
        response = requests.post(url=CHATBOT_API, json={'text': message_text, 'user':user})
        return convert_watson_to_slack(json.loads(response.json()), channel_id, user)
    except Exception as e:
        raise_exception("Error while converting watson message", str(e))


# Handle different event types and connection errors
def _event_handler(event_type: str, slack_event: json):
    if event_type == "app_mention":
        bot_id, message_text = direct_mention(slack_event['event']['text'])
        channel_id = slack_event['event']['channel']
        user = slack_event['event']['user']

    elif event_type == "interactive_message":
        message_text = slack_event['actions'][0]["value"]
        channel_id = slack_event['channel']['id']
        user = slack_event['user']['id']

    else:
        raise_exception("Error while handling event", "Invalid message")

    conn_err = connect_to_watson(message_text, channel_id, user)

    if conn_err:
        return conn_err

    return make_response("Sure!", 200)
