FROM python:3.11-alpine
LABEL authors="mamba"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p ./logs
RUN touch ./logs/chats.log ./logs/consumer.log ./logs/users.log

COPY . .

