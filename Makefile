.PHONY: docker-cloud docker-local docker-build docker-run docker-push

DOCKER_TAG_VERSION ?= staging-latest
DOCKER_TAG ?= kscout/slack-client:${DOCKER_TAG_VERSION}

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
