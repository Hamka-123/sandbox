FROM python:3-slim
WORKDIR /app
COPY ./app /app/

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["python", "main.py"]