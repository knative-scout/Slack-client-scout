from typing import Dict, List, Any, Union
import json

def available_features(response: json) -> dict:
    return  {
                    "text": response['title'],
                    "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "callback_id":"feature selection",
                    "actions": [
                        {
                            "name": "games_list",
                            "text": "Pick a option...",
                            "type": "select",
                            "options": [
                                {
                                    "text": response['options'][0]['label'],
                                    "value":  response['options'][0]['value']['input']['text']
                                },
                                {
                                    "text": response['options'][1]['label'],
                                    "value": response['options'][1]['value']['input']['text']
                                },
                                {
                                    "text": response['options'][2]['label'],
                                    "value": response['options'][2]['value']['input']['text']
                                }
                            ]
                        }
                    ]
                }


    return features