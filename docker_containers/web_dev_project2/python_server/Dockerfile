FROM python:3.14-alpine

WORKDIR /app

COPY ./app .

EXPOSE 8000

CMD ["python","-m", "http.server","8000", "--directory", "../http_root"]

