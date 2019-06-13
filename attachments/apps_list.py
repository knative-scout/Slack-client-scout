import json


def create_apps_buttons(response: json):
    options_arr = []

    for i in range(len(response['apps'])):
        options_arr.append(
            {
                "name": "apps_list",
                "text": str(response['apps'][i]['name']),
                "type": "button",
                "value": str(response['apps'][i]['app_id'])
            })
    return options_arr

def create_apps_info(response):
    res = []

    for i in range(len(response['apps'])):
        res.append(
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#36a64f",
            "author_name": "Github",
            "author_link": response['apps'][i]['github_url'],
            "author_icon": response['apps'][i]['logo_url'],
            "title": response['apps'][i]['name'],
            "title_link": response['apps'][i]['github_url'],
            "text": response['apps'][i]['tagline'],
            "fields": [
                {
                    "title": "Verification-status",
                    "value": response['apps'][i]['verification_status'],
                    "short": False
                }
            ],
            "image_url": response['apps'][i]['logo_url'],
            "thumb_url": response['apps'][i]['logo_url'],
            "footer": "Kscout",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",

        }
        )
    return res

def available_apps(response: json) :
    apps = {
        "text": "",
        "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "apps selection",
        "actions": create_apps_buttons(response)
    }

    return apps
