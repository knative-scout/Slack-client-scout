.PHONY: docker-cloud docker-local docker-build docker-run docker-push production staging

DOCKER_TAG_VERSION ?= staging-latest
DOCKER_TAG ?= kscout/slack-client:${DOCKER_TAG_VERSION}

NAMESPACE ?= kscout
POD ?= staging-slack-client

PROD_NAMESPACE ?= kscout
PROD_POD ?= prod-slack-client

# Build and Push to docker hub
docker-cloud: docker-build docker-push


# build Docker image
docker-build:
	docker build -t ${DOCKER_TAG} .


# Push the docker image for bot-api to docker hub
docker-push:
	docker push ${DOCKER_TAG}


# Runs the bot-api docker image on local machine
docker-run:
	docker run -it --rm -e BOTUSER_TOKEN=${BOTUSER_TOKEN} --net host ${DOCKER_TAG}

#Staging the app
staging: docker-cloud staging-rollout

# Deploy code to Production:
production:
	./deploy/deploy.sh -n ${PROD_NAMESPACE} -p ${PROD_POD} -t prod

#deploy code to staging:
staging-rollout:
	./deploy/deploy.sh -n ${NAMESPACE} -p ${POD} -t staging
