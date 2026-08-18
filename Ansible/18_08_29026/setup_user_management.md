cat << 'OUTER_EOF' > setup_user_management.sh
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
- name: User Management with Complex Loops
  hosts: webservers
  become: true

  vars:
    developers:
      - name: alice
        group: devops
      - name: bob
        group: developers

  tasks:
    - name: Ensure target user groups exist
      group:
        name: "{{ item.group }}"
        state: present
      loop: "{{ developers }}"

    - name: Create developer accounts
      user:
        name: "{{ item.name }}"
        group: "{{ item.group }}"
        shell: /bin/bash
        state: present
      loop: "{{ developers }}"
EOF

echo "[4/4] Запускаем Ansible плейбук..."
ansible-playbook -i inventory.ini playbook.yml
OUTER_EOF

chmod +x setup_user_management.sh
./setup_user_management.sh