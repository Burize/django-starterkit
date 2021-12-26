# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install pip==20.3.3 && pip install pipenv
COPY ./Pipfile* ./
RUN pipenv install --system