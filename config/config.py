import os
from slack import WebClient


# Setting Up ENV
bot_token = os.environ['BOTUSER_TOKEN']
verify_token = os.environ['VERIFICATION_TOKEN']
CHATBOT_API = "https://bot.kscout.io/messages"


slack = WebClient(token=bot_token)

