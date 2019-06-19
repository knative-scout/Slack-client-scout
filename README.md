# Slack-client-scout
Slack interface for chatbot api

# chat-bot-api
API which manages user conversation with virtual assistant


# Table Of Contents
- [Overview](#overview)
- [Development](#development)
- [Deployment](#deployment)

# Overview
HTTP RESTful API.

Requests pass data via JSON encoded bodies except for in GET requests where data will be passed via URL and query parameters.

Responses will always return JSON.

A user can make use of chatbot to fulfill three major purposes:
- <b>Learn :</b> Users can ask chatbot questions regarding serverless, knative, openshift and related queries.
- <b>Search :</b> Users can search for apps on https://www.kscout.io platform using chatbot
- <b>Deploy :</b> Users can ask chatbot to deploy apps that are available on the platform.

## Watson Assistant API
chatbot-api makes use of IBM`s watson api to create conversations. It uses natural language understanding, and integrated dialog tools to create conversation flows between serverless-registry-api and users.


# Development
The Chatbot API server can be run locally.  

[Configuration](#configuration),
and [Run](#run) sections.





## Configuration
For local developement follow the steps below:
- Create a Slack App
- Create a Botuser
-Configuration is passed via environment variables.
- `BOTUSER_TOKEN` : API key assigned to the bot
- `VERIFICATION_TOKEN` :Unique id given to requests coming from slack
- To access events in slack, create a public url using `ngork`

## Run
Start the server by running:

```
pip install -r requirements.txt
```

```
python app.py
```

# Deployment
