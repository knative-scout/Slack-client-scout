FROM python:3.7-alpine as base

FROM base as builder

RUN mkdir /install
WORKDIR /install

RUN apk update

RUN apk add libffi-dev openssl-dev gcc build-base

COPY requirements.txt /srv/slack_client/requirements.txt
RUN pip install -r /srv/slack_client/requirements.txt


FROM base

COPY --from=builder /usr /usr
COPY . /srv/slack_client

WORKDIR /srv/slack_client
RUN chmod 777 /srv/slack_client
RUN chmod 777 gunicornstart.sh

EXPOSE 8080

CMD ["./gunicornstart.sh"]