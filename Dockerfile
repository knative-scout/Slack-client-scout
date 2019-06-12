FROM python:3.7-slim

COPY . /srv/slack_client
WORKDIR /srv/slack_client

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-pip python3-dev \
    && apt-get -y install build-essential

RUN pip3 install -r requirements.txt

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache


RUN chmod -R 777 /var/log/nginx /var/run /var/lib/nginx \
     && chgrp -R 0 /etc/nginx \
     && chmod -R g+rwX /etc/nginx

RUN rm -v /etc/nginx/nginx.conf
COPY deploy/nginx.conf /etc/nginx

RUN chmod 777 ./nginxstart.sh

CMD ["nginx", "-g", "daemon off;"]

EXPOSE 8080

CMD ["./nginxstart.sh"]