import json
from attachments import available_features
from config.config import slack
from flask import Response


# Function to create detailed list of searched apps
def list_apps(response: Response) -> str:
    res = ""
    for i in range(len(response['apps'])):
        res += "*App name:* " + response["apps"][i]["name"] + "\n*id:* " + response["apps"][i][
            "id"] + "\n*Description:* " + response["apps"][i]["description"] + "\n*Github:* " + response["apps"][i][
                   "github_url"] + "\n\n"
    return res


# Function to create slack responses from app-api response
def convert_watson_to_slack(response: json, channel_id: str):
    try:
        response = json.loads(response.text)

        # Handle options parameter from watson
        if 'options' in response:
            slack.chat_postMessage(
                channel=channel_id,
                attachments=[available_features.available_features(response)],
            )
        # compound message with watson api and app api responses
        else:
            slack.chat_postMessage(
                channel=channel_id,
                text=list_apps(response) + "\n" + response["text"]
            )

    # generic text reply
    except:
        slack.chat_postMessage(
            channel=channel_id,
            text=response["text"],
        )
