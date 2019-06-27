FROM python:3.7-slim as base

FROM base as builder

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-pip python3-dev \
    && apt-get -y install build-essential

COPY requirements.txt /srv/bot_api/requirements.txt
RUN pip install -r /srv/bot_api/requirements.txt


FROM base
COPY --from=builder /usr /usr
COPY --from=builder /etc /etc
COPY --from=builder /var/lib/nginx /var/lib/nginx
COPY --from=builder /var/log/nginx /var/log/nginx
COPY . /srv/slack_client

WORKDIR /srv/slack_client


RUN rm /etc/nginx/sites-enabled/default

RUN chmod -R 777 /var/log/nginx /var/run /var/lib/nginx \
     && chgrp -R 0 /etc/nginx \
     && chmod -R g+rwX /etc/nginx

RUN rm -v /etc/nginx/nginx.conf
COPY deploy/nginx.conf /etc/nginx

RUN chmod 777 ./nginxstart.sh

CMD ["nginx", "-g", "daemon off;"]

EXPOSE 8080

CMD ["./nginxstart.sh"]