from flask import request, make_response, Response
import json
from event import _event_handler
from config.config import verify_token
from config import errors


# Handle post requests from slack when user interacts with buttons/ menu
def get_interactive_responses() -> Response:
    form_json = json.loads(request.form["payload"])
    verify_slack_token(form_json["token"])

    return _event_handler(form_json['type'], form_json)


# Handle post requests from slack when user writes simple text
def get_generic_responses() -> Response:
    slack_event = request.get_json()

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":"application/json"})
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    return make_response(errors.SLACK_EVENT_ERR, 404, {"X-Slack-No-Retry": 1})


# Verify if requests are coming from slack
def verify_slack_token(request_token : str) -> Response :
    if verify_token != request_token:
        return make_response(errors.SLACK_VERIFICATION_ERR, 403)

