# pull official base image
FROM python:3.8.10-buster

# set work directory
WORKDIR /usr/src/accuknowx_assignment/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gdal-bin binutils libproj-dev libgdal-dev && \
    apt-get install -y libpq-dev postgresql-client && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/accuknowx_assignment/requirements.txt
RUN pip install -r /usr/src/accuknowx_assignment/requirements.txt

# copy project
COPY . /usr/src/accuknowx_assignment/
VOLUME /usr/src/accuknowx_assignment/media
