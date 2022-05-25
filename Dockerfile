FROM python:3.8

COPY . /app/
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN ./scripts/entrypoint.sh