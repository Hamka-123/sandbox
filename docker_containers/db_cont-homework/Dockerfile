FROM ubuntu:22.04
 
LABEL Name=xampp Version=0.0.2
ENV DEBIAN_FRONTEND=noninteractive
ENV XAMPP_URL="https://sourceforge.net/projects/xampp/files/XAMPP%20Linux/8.2.12/xampp-linux-x64-8.2.12-0-installer.run/download"
 
# 1. Инсталляция со всеми нужными зависимостями
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        net-tools \
        libaio1 \
        libc6-i386 \
        libpcre3 \
        ca-certificates && \
    wget -O /tmp/xampp-installer.run "$XAMPP_URL" && \
    chmod +x /tmp/xampp-installer.run && \
    /tmp/xampp-installer.run --mode unattended && \
    # Сразу фиксим права доступа для MySQL, чтобы волюмы работали лучше
    chown -R mysql:mysql /opt/lampp/var/mysql && \
    # Cleanup
    rm /tmp/xampp-installer.run && \
    rm -rf /var/lib/apt/lists/*
 
# 2. Твики конфигурации (Пароль и Доступ к phpMyAdmin)
RUN sed -i 's/keystore_password=/keystore_password=xampp/g' /opt/lampp/properties.ini && \
    sed -i 's/Require local/Require all granted/g' /opt/lampp/etc/extra/httpd-xampp.conf
 
WORKDIR /opt/lampp
 
# Важно: файлы в этих папках будут жить на твоем Маке
VOLUME ["/opt/lampp/var/mysql", "/opt/lampp/htdocs"]
 
EXPOSE 80 443 3306
 
# 4. Запуск (используем tail -f /dev/null, если логи еще не созданы)
CMD ["/bin/bash", "-c", "/opt/lampp/lampp start && tail -f /dev/null"]