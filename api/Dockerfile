FROM python:3.10.6-alpine3.16

WORKDIR /api

COPY src /api/src
COPY templates /api/templates
COPY requirements.txt /api/

RUN rm /etc/apk/repositories && \
    echo https://dl-cdn.alpinelinux.org/alpine/v3.17/main >> /etc/apk/repositories && \
    echo https://dl-cdn.alpinelinux.org/alpine/v3.17/community >> /etc/apk/repositories && \
    apk update && \
    apk add --no-cache mariadb-connector-c-dev mariadb-connector-c && \
    apk add --virtual build-deps python3-dev gcc g++ make cmake linux-headers && \
    apk add --no-cache py3-opencv && \
    pip install -r requirements.txt && \
    pip cache purge && \
    apk del build-deps && \
    rm -rf /var/cache/apk/*

VOLUME /csvFiles

EXPOSE 7001

CMD python src/main.py