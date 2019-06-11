from slack import WebClient
from flask import Flask, request, make_response
from config.config import bot_token

slack = WebClient(bot_token)
app = Flask(__name__)


def _event_handler(event_type, slack_event):
    if event_type == "direct_mention":
        user_id = slack_event["event"]["user"]["id"]
        channel_id = slack_event["event"]

        return make_response("Welcome Message Sent", 200, )


@app.route("/listening", methods=["GET", "POST"])
def incoming_messages():
    slack_event = request.get_json()
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
