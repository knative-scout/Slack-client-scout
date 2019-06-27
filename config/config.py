import os
from slack import WebClient
import logging

bot_token = os.environ['BOTUSER_TOKEN']

slack = WebClient(token=bot_token)

verify_token = os.environ['VERIFICATION_TOKEN']

CHATBOT_API = "https://bot.kscout.io/messages"


# Logging Config

logger = logging.getLogger("slack-api-logger")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# Add logs to file
logFile = "app.log"
fmt = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(name)s-%(levelname)s: %(message)s'
logFormatter = logging.Formatter(fmt)

fileHandler = logging.FileHandler(logFile)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
