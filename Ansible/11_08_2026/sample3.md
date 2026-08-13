cat << EOT > run.sh
#!/usr/bin/env bash
set -e

apt update && apt install -y ansible

echo "=== 1. Creating directory structure ==="
mkdir -p templates group_vars host_vars

echo "=== 2. Creating Jinja2 Template (templates/index.html.j2) ==="
cat << 'EOF' > templates/index.html.j2
<!DOCTYPE html>
<html>
<head>
    <title>{{ site_title | default('Default Server Title') }}</title>
</head>
<body>
    <h1>Server Information Card</h1>
    <ul>
        <li><strong>Hostname:</strong> {{ ansible_hostname }}</li>
        <li><strong>OS:</strong> {{ ansible_distribution }} {{ ansible_distribution_version }}</li>
        
        {#
          ОШИБКА/ЗАГАДКА №1: В Docker-контейнерах факты сети (ansible_default_ipv4) 
          могут отсутствовать или быть пустыми. Вызов напрямую .address упадет с UndefinedError.
          ПРЕПОД: <li><strong>IP Address:</strong> {{ ansible_default_ipv4.address }}</li>
        #}
        <li><strong>IP Address:</strong> {{ ansible_default_ipv4.address | default('N/A') }}</li>
        <li><strong>Total Memory:</strong> {{ ansible_memtotal_mb | default('N/A') }} MB</li>
        <li><strong>Core Count:</strong> {{ ansible_processor_vcpus | default('N/A') }}</li>
    </ul>

    <h3>Active Services:</h3>
    <ul>
    {#
      ОШИБКА/ЗАГАДКА №2: Если хост не попал в группу [webservers], active_services не считается 
      и цикл {% for %} упадет на UndefinedError.
      ПРЕПОД: {% for service in active_services %}
    #}
    {% for service in active_services | default([]) %}
        <li>{{ service }}</li>
    {% endfor %}
    </ul>
</body>
</html>
EOF

echo "=== 3. Creating Group Variables (group_vars/webservers.yml) ==="
cat << 'EOF' > group_vars/webservers.yml
# ПРЕПОД: Переменная site_title зашита в group_vars, из-за чего у всех хостов одинаковый title.
# site_title: "Automated DevOps Node"

active_services:
  - Nginx Web Server
  - Firewall Security Module
  - System Telemetry Collector
EOF

echo "=== 4. Creating Host Variables for custom <title> per node ==="
# Правильный подход: переопределяем site_title индивидуально для каждого хоста
cat << 'EOF' > host_vars/node1.yml
site_title: "Custom Title for Node 1 (Primary)"
EOF

cat << 'EOF' > host_vars/node2.yml
site_title: "Custom Title for Node 2 (Secondary)"
EOF

echo "=== 5. Creating Inventory (inventory.ini) ==="
cat << 'EOF' > inventory.ini
[webservers]
node1 ansible_connection=docker ansible_python_interpreter=/usr/bin/python3
node2 ansible_connection=docker ansible_python_interpreter=/usr/bin/python3
EOF

echo "=== 6. Creating Playbook (deploy_custom_site.yml) ==="
cat << 'EOF' > deploy_custom_site.yml
---
- name: Deploy Custom Web Page to Webservers
  hosts: webservers
  
  # ОШИБКА/ЗАГАДКА №3: Если поставить gather_facts: false, все факты ansible_* упадут.
  gather_facts: true

  tasks:
    # --- ПРОВЕРКИ СТАТУСА NGINX ---
    - name: Check if Nginx package is installed
      ansible.builtin.package:
        name: nginx
        state: present

    - name: Ensure Nginx service is running and enabled
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true

    - name: Verify Nginx process status via command
      ansible.builtin.command: pgrep nginx
      register: nginx_proc_check
      changed_when: false
      failed_when: nginx_proc_check.rc != 0

    - name: Ensure target directory exists
      ansible.builtin.file:
        path: /var/www/html
        state: directory
        mode: '0755'

    # --- ДЕПЛОЙ ШАБЛОНА ---
    # ОШИБКА/ЗАГАДКА №4 (Главная "загадка" преподавателя): Использование модуля copy вместо template.
    # ПРЕПОД:
    # - name: Deploy file
    #   ansible.builtin.copy:
    #     src: templates/index.html.j2
    #     dest: /var/www/html/index.html
    #     mode: '0644'
    # (При использовании copy файл скопируется с нераскрытыми {{ переменными }} и циклом {% for %})

    - name: Render Jinja2 template to index.html
      ansible.builtin.template:
        src: templates/index.html.j2
        dest: /var/www/html/index.html
        mode: '0644'
EOF

echo "=== 7. Starting Docker Nodes (node1 & node2) ==="
docker rm -f node1 node2 2>/dev/null || true

docker run -d --name node1 -p 8081:80 ubuntu:22.04 bash -c "apt-get update && apt-get install -y nginx python3 && nginx -g 'daemon off;'"
docker run -d --name node2 -p 8082:80 ubuntu:22.04 bash -c "apt-get update && apt-get install -y nginx python3 && nginx -g 'daemon off;'"
echo "Waiting for containers to initialize..."
sleep 5

echo "=== Setup complete! ==="
echo "Run playbook with: ansible-playbook -i inventory.ini deploy_custom_site.yml"
EOT

chmod +x run.sh
./run.sh

ansible-playbook -i inventory.ini deploy_custom_site.yml
docker exec node1 cat /var/www/html/index.html
docker exec node2 cat /var/www/html/index.html