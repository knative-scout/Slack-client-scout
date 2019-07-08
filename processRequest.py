from flask import request
from event import _event_handler
from config.config import verify_token
from config.panic import *


# Handle post requests from slack when user interacts with buttons/ menu
def get_interactive_responses():
    try:
        form_json = json.loads(request.form["payload"])

        if not verify_slack_token(form_json["token"]):
            raise_exception("Slack Verification Error", "Invalid Slack Token")

        return _event_handler(form_json['type'], form_json)
    except Exception as e:
        raise_exception("Exception while handling Interactive Message", str(e))


# Handle post requests from slack when user writes simple text
def get_generic_responses():
    try:
        slack_event = request.get_json()
        print(slack_event)

        if "challenge" in slack_event:
            return slack_event["challenge"]

        if "event" in slack_event:
            event_type = slack_event["event"]["type"]

            if event_type == "app_mention" or event_type == "interactive_message":
                return _event_handler(event_type, slack_event)

        raise_exception("Error In Generic Response", "No Event")
    except Exception as e:
        raise_exception("Exception while handling Generic Message", str(e))


# Verify if requests are coming from slack
def verify_slack_token(request_token : str):
    if verify_token == request_token:
        return True


