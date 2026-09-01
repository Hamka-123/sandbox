#!/bin/bash
set -e

# Очищаем папку, если запускаем скрипт не в первый раз, чтобы избежать конфликтов
rm -rf ansible-exam-lab

echo "==> Обновление списка пакетов..."
sudo apt-get update

echo "==> Установка Ansible, Python и сопутствующих утилит..."
sudo apt-get install -y ansible python3-pip python3-yaml curl htop unzip

echo "==> Проверка версии Ansible..."
ansible --version

# Phase 1: Environment & Inventory Setup
# 1. Create a directory named ansible-exam-lab and navigate into it.
echo "==> Создание директории ansible-exam-lab..."
mkdir ansible-exam-lab
cd ansible-exam-lab

# 2. Create an INI inventory file named inventory.ini
echo "==> Создание inventory.ini..."
cat << 'EOF' > inventory.ini
[webservers]
node1 ansible_host=127.0.0.1
node2 ansible_host=127.0.0.1

[database]
node1 ansible_host=127.0.0.1

[production:children]
webservers
database
EOF

# 3. Create a hidden vault password file named .vault_pass without a trailing newline. Set permissions to 600.
echo "==> Создание .vault_pass..."
printf "ExamVaultSecret2026" > .vault_pass
chmod 600 .vault_pass

# 4. Ensure .vault_pass is added to a .gitignore file.
echo "==> Создание .gitignore..."
echo ".vault_pass" > .gitignore


# Phase 2: Role Creation & Templating
echo "==> Создание роли webapp..."
# 1. Scaffold a role named webapp inside a roles/ directory.
mkdir -p roles/webapp/{defaults,handlers,tasks,templates}
# or ansible-galaxy init roles/webapp

# 2. Define default variables
cat << 'EOF' > roles/webapp/defaults/main.yml
---
app_port: 80
app_title: "Enterprise Portal"
EOF

# 3. Create a Jinja2 template
cat << 'EOF' > roles/webapp/templates/index.html.j2
<!DOCTYPE html>
<html>
<head>
    <title>{{ app_title }}</title>
</head>
<body>
    <h1>{{ app_title }}</h1>
    <p>Host Name: {{ ansible_hostname }}</p>
    <p>IP Address: {{ ansible_default_ipv4.address | default('127.0.0.1') }}</p>
    
    <h2>Active Web Servers:</h2>
    <ul>
    {% for host in groups['webservers'] %}
        <li>{{ host }}</li>
    {% endfor %}
    </ul>
</body>
</html>
EOF

# 4. Configure tasks
cat << 'EOF' > roles/webapp/tasks/main.yml
---
- name: Update package manager cache dynamically based on OS family (Debian)
  apt:
    update_cache: yes
  when: ansible_facts['os_family'] == 'Debian'

- name: Update package manager cache dynamically based on OS family (RedHat)
  dnf:
    update_cache: yes
  when: ansible_facts['os_family'] == 'RedHat'

- name: Install the appropriate web server (Debian)
  apt:
    name: apache2
    state: present
  when: ansible_facts['os_family'] == 'Debian'

- name: Install the appropriate web server (RedHat)
  dnf:
    name: httpd
    state: present
  when: ansible_facts['os_family'] == 'RedHat'

- name: Set service name fact based on OS
  set_fact:
    web_service_name: "{{ 'apache2' if ansible_facts['os_family'] == 'Debian' else 'httpd' }}"

- name: Deploy index.html.j2 to the web root
  template:
    src: index.html.j2
    dest: /var/www/html/index.html
    mode: '0644'
  notify: restart web server
EOF

cat << 'EOF' > roles/webapp/handlers/main.yml
---
- name: restart web server
  service:
    name: "{{ web_service_name }}"
    state: restarted
    enabled: true
EOF

# Trigger a handler to ensure the web service is running and enabled.
# ansible-playbook -i inventory.ini site_deploy.yml --vault-password-file .vault_pass

# Phase 3: Resilient Logic & Error Handling
echo "==> Создание maintenance_check.yml..."
cat << 'EOF' > maintenance_check.yml
---
- name: Pre-flight System Checks
  hosts: all
  become: true
  tasks:
    - name: Install system diagnostic utilities
      package:
        name: "{{ item }}"
        state: present
      loop:
        - curl
        - htop
        - unzip

    - name: Disk space check block
      block:
        - name: Check available disk space on /
          shell: df -h / | awk 'NR==2 {print $5}' | sed 's/%//'
          register: disk_usage
          changed_when: false
          failed_when: disk_usage.stdout | int > 80

      rescue:
        - name: Display warning message
          debug:
            msg: "Disk usage threshold exceeded! Triggering automated log cleanup..."

      always:
        - name: Create a log file appending an ISO-8601 execution timestamp
          shell: date --iso-8601=seconds >> /tmp/maintenance.log
          changed_when: false
          delegate_to: localhost
EOF

# Run maintenance_check.yml
# ansible-playbook -i inventory.ini maintenance_check.yml --vault-password-file .vault_pass

# Phase 4: Security & Vault Controls
echo "==> Создание зашифрованного vault.yml и deploy_db_credentials.yml..."
mkdir -p group_vars/production

# 1. & 2. Create and include encrypted keys
cat << 'EOF' > group_vars/production/vault.yml
vault_db_user: "db_admin"
vault_db_pass: "P@ssw0rd_Exam_2026!"
EOF

ansible-vault encrypt group_vars/production/vault.yml --vault-password-file .vault_pass

# 3. Create a playbook named deploy_db_credentials.yml
cat << 'EOF' > deploy_db_credentials.yml
---
- name: Deploy DB Credentials
  hosts: database
  become: true
  tasks:
    - name: Deploy a configuration file containing the rendered database credentials
      copy:
        content: |
          DB_USER={{ vault_db_user }}
          DB_PASSWORD={{ vault_db_pass }}
        dest: /etc/db_app.conf
        mode: '0600'
      no_log: true
EOF

# Run
# ansible-playbook -i inventory.ini deploy_db_credentials.yml --vault-password-file .vault_pass

# Phase 5: Enterprise Orchestration & Rolling Upgrades
echo "==> Создание site_deploy.yml..."
cat << 'EOF' > site_deploy.yml
---
- name: Master Orchestration - Zero-Downtime Rolling Deployment
  hosts: webservers
  become: true
  serial: 1

  pre_tasks:
    - name: Print removing from load balancer message
      debug:
        msg: "Removing {{ inventory_hostname }} from service load balancer..."

  roles:
    - role: webapp

  post_tasks:
    - name: Include a URI health check verifying HTTP 200
      uri:
        url: "http://localhost:80"
        status_code: 200
        return_content: yes
      
    - name: Print re-adding to load balancer message
      debug:
        msg: "Re-adding {{ inventory_hostname }} back to load balancer..."
EOF

# Run
# ansible-playbook -i inventory.ini site_deploy.yml --vault-password-file .vault_pass


echo "==> Структура проекта полностью и корректно создана в ansible-exam-lab!"