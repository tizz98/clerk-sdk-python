FROM python:3.11.4-alpine3.18
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1

WORKDIR /app
RUN apk add musl-dev linux-headers gcc g++ zlib-dev libffi-dev

RUN pip install --no-cache-dir poetry 

COPY ./pyproject.toml /app/
COPY ./poetry.lock /app/

ARG VERSION
ENV VERSION $VERSION


RUN poetry install

COPY . .
