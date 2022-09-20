FROM python:3.10.7-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV TZ="Asia/Shanghai"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends default-libmysqlclient-dev gcc libffi-dev make git && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    pip install poetry

COPY pyproject.toml poetry.lock main.py /app/
COPY src /app/src
COPY data.db /app/data.db

RUN poetry install