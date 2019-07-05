.PHONY: push \
	rollout rollout-prod rollout-staging \
	imagestream-tag \
	deploy deploy-prod deploy-staging \
	rm-deploy \
	docker docker-build docker-push


MAKE ?= make

APP ?= slack-client
DOCKER_TAG ?= kscout/${APP}:${ENV}-latest

KUBE_LABELS ?= app=${APP},env=${ENV}
KUBE_TYPES ?= dc,configmap,secret,deploy,statefulset,svc,route,is,pod,pv,pvc

KUBE_APPLY ?= oc apply -f -


#push local code to ENV deploy
push: docker imagestream-tag

# rollout ENV
rollout:
	@if [ -z "${ENV}" ]; then echo "ENV must be set"; exit 1; fi
	oc rollout latest dc/${ENV}-${APP}

# rollout production
rollout-prod:
	${MAKE} rollout ENV=prod

# rollout staging
rollout-staging:
	${MAKE} rollout ENV=staging

# import latest tag for ENV to imagestream
imagestream-tag:
	@if [ -z "${ENV}" ]; then echo "ENV must be set"; exit 1; fi
	oc tag docker.io/kscout/${APP}:${ENV}-latest ${ENV}-${APP}:${ENV}-latest --scheduled

# deploy to ENV
deploy:
	@if [ -z "${ENV}" ]; then echo "ENV must be set"; exit 1; fi
	helm template \
		--values deployHelm/values.yaml \
		--values deployHelm/values.secrets.${ENV}.yaml \
		--set global.env=${ENV} deployHelm \
	| ${KUBE_APPLY}

# deploy to production
deploy-prod:
	${MAKE} deploy ENV=prod

# deploy to staging
deploy-staging:
	${MAKE} deploy ENV=staging

# remove deployment for ENV
rm-deploy:
	@if [ -z "${ENV}" ]; then echo "ENV must be set"; exit 1; fi
	@echo "Remove ${ENV} ${APP} deployment"
	@echo "Hit any key to confirm"
	@read confirm
	oc get -l ${KUBE_LABELS} ${KUBE_TYPES} -o yaml | oc delete -f -

# build and push docker image
docker: docker-build docker-push

# build docker image for ENV
docker-build:
	@if [ -z "${ENV}" ]; then echo "ENV must be set"; exit 1; fi
	docker build -t ${DOCKER_TAG} .

# push docker image for ENV
docker-push:
	@if [ -z "${ENV}" ]; then echo "ENV must be set"; exit 1; fi
	docker push ${DOCKER_TAG}



##########################################################################
#Old Methods in Makefile
##########################################################################

DOCKER_TAG_VERSION ?= staging-latest
DOCKER_TAG_C ?= kscout/slack-client:${DOCKER_TAG_VERSION}

NAMESPACE ?= kscout
POD ?= staging-slack-client

PROD_NAMESPACE ?= kscout
PROD_POD ?= prod-slack-client

# Build and Push to docker hub
docker-cloud-classic: docker-build-classic docker-push-classic


# build Docker image
docker-build-classic:
	docker build -t ${DOCKER_TAG_C} .


# Push the docker image for bot-api to docker hub
docker-push-classic:
	docker push ${DOCKER_TAG_C}


# Runs the bot-api docker image on local machine
docker-run-classic:
	docker run -it --rm -e BOTUSER_TOKEN=${BOTUSER_TOKEN} -e VERIFICATION_TOKEN={VERIFICATION_TOKEN} --net host ${DOCKER_TAG_C}

#Staging the app
staging-classic: docker-cloud-classic staging-rollout-classic

# Deploy code to Production:
production-classic:
	./deploy/deploy.sh -n ${PROD_NAMESPACE} -p ${PROD_POD} -t prod

#deploy code to staging:
staging-rollout-classic:
	./deploy/deploy.sh -n ${NAMESPACE} -p ${POD} -t staging