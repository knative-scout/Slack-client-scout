import json


def create_buttons(response: json) -> dict:
    actions=[]
    for i in range(len(response['options'])):
        item = {
                "name": "feature_list",
                "text": response['options'][i]['label'],
                "type": "button",
                "value": response['options'][i]['value']['input']['text']
            }
        actions.append(item)
    features = {
        "text": response['title'],
        "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "feature selection",
        "actions": actions
    }

    return features


# only allow maximum of 10 buttons
def create_buttons_gt_limit(response: json) -> dict:

    if len(response['options']) <= 10:
        actions = []
        for i in range(len(response['options'])):
            item = {

                "text": response['options'][i]['label'],

                "value": response['options'][i]['value']['input']['text']
            }
            actions.append(item)
        features = {
            "text": response['title'],
            "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "feature selection",
            "actions": [ {
                    "name": "questions_list",
                    "text": "Pick a question...",
                    "type": "select",
                    "options": actions
            }
            ]
        }

        return features
    return {}



