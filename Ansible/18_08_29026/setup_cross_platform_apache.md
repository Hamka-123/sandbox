cat << 'OUTER_EOF' > setup_cross_platform_apache.sh
#!/bin/bash
set -e

echo "[1/4] Проверяем и устанавливаем Ansible..."
if ! command -v ansible-playbook &> /dev/null; then
    apt update && apt install -y ansible
fi

echo "[2/4] Создаем inventory.ini..."
cat << 'EOF' > inventory.ini
[webservers]
localhost ansible_connection=local
EOF

echo "[3/4] Создаем playbook.yml..."
cat << 'EOF' > playbook.yml
---
- name: Cross-Platform Web Server Setup
  hosts: webservers
  become: true

  tasks:
    - name: Install Apache on Debian/Ubuntu systems
      apt:
        name: apache2
        state: present
        update_cache: yes
      when: ansible_facts['os_family'] == "Debian"

    - name: Install Apache on RedHat/CentOS systems
      dnf:
        name: httpd
        state: present
      when: ansible_facts['os_family'] == "RedHat"

    - name: Ensure Apache is running (Debian)
      service:
        name: apache2
        state: started
      when: ansible_facts['os_family'] == "Debian"

    - name: Ensure Apache is running (RedHat)
      service:
        name: httpd
        state: started
      when: ansible_facts['os_family'] == "RedHat"
EOF

echo "[4/4] Запускаем Ansible плейбук..."
ansible-playbook -i inventory.ini playbook.yml
OUTER_EOF

chmod +x setup_cross_platform_apache.sh
./setup_cross_platform_apache.sh