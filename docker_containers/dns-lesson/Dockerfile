FROM alpine:latest

RUN apk update && \
apk add --no-cache \
bash \
iputils \
bind-tools \
busybox-extras

WORKDIR /app
COPY . .

EXPOSE 8888

CMD ["bash"]
