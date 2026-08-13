FROM python:3.11-slim

LABEL name=Python-client version=1.0.0

WORKDIR /app
COPY ./app /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
chown -R appuser /app

USER appuser

RUN pip3 install --no-cache-dir mysql-connector-python


CMD [ "python","main.py" ]