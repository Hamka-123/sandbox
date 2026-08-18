cat << 'OUTER_EOF' > run_error_demo.sh
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
- name: Demonstrate Advanced Error Control
  hosts: webservers
  tasks:

    # 1. Ignore errors for non-critical health checks
    - name: Ping an external host (Allowed to fail)
      command: ping -c 2 10.255.255.1
      ignore_errors: true

    # 2. Suppress false "changed" states for read-only commands
    - name: Check system uptime
      command: uptime
      changed_when: false    # Prevents Ansible from marking read-only checks as "changed"

    # 3. Define custom failure conditions based on command output
    - name: Check available disk space on root partition
      shell: df -h / | awk 'NR==2 {print $5}' | sed 's/%//'
      register: disk_usage
      changed_when: false
      failed_when: disk_usage.stdout | int > 90   # Fail ONLY if disk usage > 90%

    - name: Display disk check result
      debug:
        msg: "Root disk usage is currently at {{ disk_usage.stdout }}%"
EOF

echo "[4/4] Запускаем Ansible плейбук..."
ansible-playbook -i inventory.ini playbook.yml
OUTER_EOF

chmod +x run_error_demo.sh
./run_error_demo.sh