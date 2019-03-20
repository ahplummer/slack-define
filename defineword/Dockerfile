FROM alpine:3.9

ADD ./*.* /defineword/

RUN apk add --no-cache python3 bash

RUN cd /defineword && pip3 install -r requirements.txt

WORKDIR /defineword
