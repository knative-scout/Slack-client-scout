import os
from slack import WebClient


bot_token= os.environ['BOTUSER_TOKEN']

slack = WebClient(bot_token)

verify_token = os.environ['VERIFICATION_TOKEN']

CHATBOT_API="http://localhost:8080/messages"
