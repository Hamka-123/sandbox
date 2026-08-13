FROM ubuntu:22.04
 
LABEL Name=xampp Version=0.0.2
ENV DEBIAN_FRONTEND=noninteractive
ENV XAMPP_URL="https://sourceforge.net/projects/xampp/files/XAMPP%20Linux/8.2.12/xampp-linux-x64-8.2.12-0-installer.run/download"
 
# 1. Combine updates, installs, and XAMPP installation into one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        net-tools \
        libaio1 \
        libc6-i386 \
        libpcre3 \
        ca-certificates && \
    # Download and Install in the same layer to keep the image slim
    wget -O /tmp/xampp-installer.run "$XAMPP_URL" && \
    chmod +x /tmp/xampp-installer.run && \
    /tmp/xampp-installer.run --mode unattended && \
    # Cleanup: Delete the installer AND the apt lists in the SAME layer
    rm /tmp/xampp-installer.run && \
    rm -rf /var/lib/apt/lists/*
 
# 2. Configuration tweaks
RUN sed -i 's/keystore_password=/keystore_password=xampp/g' /opt/lampp/properties.ini
 
# 3. Set Working Directory
WORKDIR /opt/lampp
 
VOLUME ["/opt/lampp/var/mysql", "/opt/lampp/htdocs"]
 
EXPOSE 80 443 3306
 
# 4. Improved Startup
# Using 'tail -f /dev/null' is sometimes more robust if error_log doesn't exist yet
CMD ["/bin/bash", "-c", "/opt/lampp/lampp start && tail -f /opt/lampp/logs/error_log"]