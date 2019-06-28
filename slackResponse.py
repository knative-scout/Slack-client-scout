import json
from attachments import available_features,apps_list
from config.config import slack,bot_token,logger
from flask import Response
from slack import errors

# Function to create detailed list of searched apps
def list_apps(response: Response) -> str:
    res = ""
    for i in range(len(response['apps'])):
        res += "*App name:* " + response["apps"][i]["name"] + "\n*id:* " + response["apps"][i][
            "app_id"] + "\n*Description:* " + response["apps"][i]["description"] + "\n*Github:* " + response["apps"][i][
                   "github_url"] + "\n\n"
    return res


# Function to create slack responses from app-api response

def convert_watson_to_slack(response: json, channel_id: str, user: str):
    response = json.loads(response.text)
    logger.debug('Slack Post Request: token - ' + str(bot_token) + ' Channel - ' + str(channel_id))
    resp =""
    # Handle options parameter from watson
    try:
        if 'options' in response:

            resp = slack.chat_postMessage(
                token=bot_token,
                channel=channel_id,
                text= '<@'+user +'>',
                attachments=[available_features.available_features(response)],
            )
        # compound message with watson api and app api responses
        elif 'apps' in response:
            resp = slack.chat_postMessage(
                token=bot_token,
                channel=channel_id,
                text = '<@'+user + '>',
                attachments=apps_list.create_apps_info(response) + [apps_list.available_apps(response)],
            )

        # generic text reply

        elif 'text' in response:
           resp = slack.chat_postMessage(
                token=bot_token,
                channel=channel_id,
                text='<@'+user + '>' + response["text"],
            )

        logger.debug("Slack Post Response: " + str(resp))

    except errors.SlackApiError as e:
        logger.debug(e)


