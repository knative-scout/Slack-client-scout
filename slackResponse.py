from attachments import available_features, apps_list
from config.panic import *


# Function to create detailed list of searched apps
def list_apps(response: Response):
    res = ""
    for i in range(len(response['apps'])):
        res += "*App name:* " + response["apps"][i]["name"] + "\n*id:* " + response["apps"][i][
            "app_id"] + "\n*Description:* " + response["apps"][i]["description"] + "\n*Github:* " + response["apps"][i][
                   "github_url"] + "\n\n"
    return res


# Function to create slack responses from app-api response

def create_slack_response(response: json):
    # Handle options parameter from API
    response = response
    try:
        # compound message with watson api and app api responses
        if 'apps' in response:
            text = ""
            attachments = apps_list.create_apps_info(response) + [apps_list.available_apps(response)]
            return text, attachments

        elif 'response_type' in response and response['response_type'] == 'option':
            text = ''
            attachments = [available_features.available_features(response)]
            return text, attachments

        # generic text reply
        elif 'text' in response:
            text = response["text"]
            attachments = None
            return text, attachments

    except Exception as e:
        raise_exception("Error while creating slack response", str(e))


