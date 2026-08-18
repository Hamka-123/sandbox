cat << 'OUTER_EOF' > setup_basic_loops.sh
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
- name: Demonstrate Basic Loops
  hosts: webservers
  become: true

  tasks:
    # TASK 1: Refresh the repository cache
    - name: Update package cache
      package:
        update_cache: yes

    # TASK 2: Loop through and install packages
    - name: Install required baseline packages
      package:
        name: "{{ item }}"
        state: present
      loop:
        - curl
        - git
        - htop
        - unzip
EOF

echo "[4/4] Запускаем Ansible плейбук..."
ansible-playbook -i inventory.ini playbook.yml
OUTER_EOF

chmod +x setup_basic_loops.sh
./setup_basic_loops.sh