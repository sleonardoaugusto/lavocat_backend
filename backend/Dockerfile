# pull official base image
FROM python:3.10.0-alpine

# set work directory
WORKDIR /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk add --no-cache postgresql-dev build-base \
 && apk update \
 && apk add bash

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN ls
# copy project
COPY . .