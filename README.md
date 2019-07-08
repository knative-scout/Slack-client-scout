# Slack-client-scout
Slack interface for chatbot api



# Table Of Contents
- [Overview](#overview)
- [Development](#development)
- [Deployment](#deployment)
- [Examples](#examples)

# Overview
Slack interface helps user to access chatbot api interactively. Users can ask queries regarding serverless, search for apps, and deploy apps using slack channel.
Following [Examples](#examples) section will walk you through some sample conversations in a slack channel using the bot.
 
# Development
The slack-client server can be run locally.  

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
- Add `/listening` to slack interactive messages and events subscription pannels

## Run
Start the server by running:

```
pip install -r requirements.txt
```

```
python app.py
```

# Deployment
## Deployment Configuration
Create a copy of `deploy/values.secrets.example.yaml` named 
`deploy/values.secrets.ENV.yaml` for whichever deployment environment you wish
to configure.

Edit this file with your own values.

Never commit this file.

## Deploy
Initialize submodules:

```
git submodule update --init --recursive
```

Deploy production by running:

```
make deploy-prod
```

If this is the first time production has been deployed run:

```
make rollout-prod
```

# Examples
