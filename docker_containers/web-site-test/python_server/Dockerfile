FROM python:3.14-alpine

COPY app /app

WORKDIR /app

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8000/ || exit 1

CMD [ "python","-m","http.server","8000","--directory","http_root" ]