from flask import request, make_response, Response
import json
from event import _event_handler
from config.config import verify_token, logger
from config import errors


# Handle post requests from slack when user interacts with buttons/ menu
def get_interactive_responses() -> Response:
    if 'payload' in request.form:
        logger.debug('User Post: ' + str(request.form['payload']))
        form_json = json.loads(request.form["payload"])

        verified_token = verify_slack_token(form_json["token"])

        if verified_token:
            return verified_token

        return _event_handler(form_json['type'], form_json)
    else:
        return make_response("Invalid Request",404)


# Handle post requests from slack when user writes simple text
def get_generic_responses() -> Response:
    slack_event = request.get_json()

    if "challenge" in slack_event:
        logger.debug(slack_event["challenge"])
        return make_response(slack_event["challenge"], 200, {"content_type":"application/json"})
    if "event" in slack_event:
        logger.debug('User Post: ' + str(slack_event["event"]))
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    return make_response(errors.SLACK_EVENT_ERR, 404, {"X-Slack-No-Retry": 1})


# Verify if requests are coming from slack
def verify_slack_token(request_token : str) -> Response :
    if verify_token != request_token:
        return make_response(errors.SLACK_VERIFICATION_ERR, 403)

