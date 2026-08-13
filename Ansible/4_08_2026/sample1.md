cat << 'EOF' > setup_and_run.sh
#!/bin/bash
set -e

echo "=== 1. Создание Dockerfile и запуск Managed Nodes ==="
cat << 'DOCKERFILE' > Dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y openssh-server sudo python3 nginx && \
    mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

EXPOSE 22 80

CMD ["/usr/sbin/sshd", "-D"]
DOCKERFILE

docker build -t ansible-node .

# Удаляем старые контейнеры, если они существовали
docker rm -f node1 node2 2>/dev/null || true

docker run -d --name node1 -p 8081:80 ansible-node
docker run -d --name node2 -p 8082:80 ansible-node

NODE1_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' node1)
NODE2_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' node2)

echo "Node1 IP: $NODE1_IP"
echo "Node2 IP: $NODE2_IP"

echo -e "\n=== 2. Установка Ansible и SSHpass на Control Node ==="
sudo apt-get update -y && sudo apt-get install -y ansible sshpass

echo -e "\n=== 3. Настройка SSH-ключей ==="
rm -f ~/.ssh/id_rsa*
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa

sshpass -p 'root' ssh-copy-id -o StrictHostKeyChecking=no root@$NODE1_IP
sshpass -p 'root' ssh-copy-id -o StrictHostKeyChecking=no root@$NODE2_IP

echo -e "\n=== 4. Создание inventory.ini ==="
cat << INVENTORY > inventory.ini
[managed_nodes]
node1 ansible_host=$NODE1_IP
node2 ansible_host=$NODE2_IP

[managed_nodes:vars]
ansible_user=root
INVENTORY

echo -e "\n=== 5. Проверка связи (Ping) ==="
ansible managed_nodes -i inventory.ini -m ping

echo -e "\n=== 6. Запись и чтение файла через ad-hoc команды ==="
ansible managed_nodes -i inventory.ini -m copy -a "content='Hello from Ansible Control Node!\n' dest=/root/greeting.txt"
ansible managed_nodes -i inventory.ini -m command -a "cat /root/greeting.txt"

echo -e "\n=== 7. Идеи от ИИ: Сбор фактов о системе ==="
ansible managed_nodes -i inventory.ini -m setup -a "filter=ansible_distribution*"

echo -e "\n=== 8. Создание playbook.yml ==="
cat << 'PLAYBOOK' > playbook.yml
---
- name: Configure Nginx on Managed Nodes
  hosts: managed_nodes
  tasks:
    - name: 1. Ensure Nginx is installed
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: 2. Create custom index.html page
      copy:
        content: |
          <!DOCTYPE html>
          <html>
          <head><title>Managed Node</title></head>
          <body>
            <h1>Hello! Managed by Ansible on {{ inventory_hostname }}</h1>
          </body>
          </html>
        dest: /var/www/html/index.html
        mode: '0644'

    - name: 3. Ensure Nginx service is started and enabled at boot
      service:
        name: nginx
        state: started
        enabled: yes
PLAYBOOK

echo -e "\n=== 9. Запуск Nginx Playbook ==="
ansible-playbook -i inventory.ini playbook.yml

echo -e "\n=== 10. Проверка работы Nginx на нодах ==="
echo "Ответ от Node1:"
curl -s http://$NODE1_IP
echo -e "\nОтвет от Node2:"
curl -s http://$NODE2_IP
echo -e "\n\n Все шаги успешно выполнены!"
EOF

chmod +x setup_and_run.sh
./setup_and_run.sh