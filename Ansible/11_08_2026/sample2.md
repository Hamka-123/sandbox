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
cat << 'PLAYBOOK' > playbook2.yml
---
---
- name: Deploy Configurable Web Server
  hosts: webservers
  become: true

  # 1. DEFINE YOUR VARIABLES HERE
  vars:
    web_port: 80
    site_title: "Welcome to DevOps Class"
    app_dir: "/var/www/html"

  tasks:
    - name: Display node system resources
      ansible.builtin.debug:
        msg:
          - "OS: {{ ansible_distribution }} {{ ansible_distribution_version }}"
          - "CPU Cores: {{ ansible_processor_vcpus }}"
          - "RAM Total: {{ ansible_memtotal_mb }} MB"
          - "IP Address: {{ ansible_default_ipv4.address | default('N/A') }}"

    - name: Ensure Nginx is installed
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Create index.html using variables
      copy:
        # Reference variables with {{ double_braces }}
        content: "<h1>{{ site_title }}</h1><p>Running on port {{ web_port }}</p>"
        dest: "{{ app_dir }}/index.html"
        mode: '0644'
    - name: Update custom Nginx config file
      copy:
        content: "server { listen {{ web_port }}; root {{ app_dir }}; }"
        dest: /etc/nginx/conf.d/custom.conf
      # 'notify' triggers the handler ONLY if this file is modified or created
      notify: Restart Nginx

  # HANDLERS SECTION (Runs at the very end of the play)
  handlers:
    - name: Restart Nginx
      service:
        name: nginx
        state: restarted
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