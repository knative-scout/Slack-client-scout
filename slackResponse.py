from attachments import available_features,apps_list
from config.config import slack, bot_token
from config.panic import *
from config.logger import *


# Function to create detailed list of searched apps
def list_apps(response: Response) -> str:
    res = ""
    for i in range(len(response['apps'])):
        res += "*App name:* " + response["apps"][i]["name"] + "\n*id:* " + response["apps"][i][
            "app_id"] + "\n*Description:* " + response["apps"][i]["description"] + "\n*Github:* " + response["apps"][i][
                   "github_url"] + "\n\n"
    return res


# Function to create slack responses from app-api response

def create_slack_response(response: json):
    # Handle options parameter from API
    try:
        if response['response_type'] == 'option':
            text = ''
            attachments = [available_features.available_features(response)]
            return text, attachments

        # compound message with watson api and app api responses
        elif 'apps' in response:
            text = ""
            attachments = apps_list.create_apps_info(response) + [apps_list.available_apps(response)]
            return text, attachments

        # generic text reply
        elif 'text' in response:
            text = response["text"]
            attachments = None
            return text, attachments

    except Exception as e:
        raise_exception("Error while creating slack response", str(e))


