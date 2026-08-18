cat << 'OUTER_EOF' > setup_multi_node_docker.sh
#!/bin/bash
set -e

echo "[1/5] Проверяем и устанавливаем Ansible на хосте..."
if ! command -v ansible-playbook &> /dev/null; then
    apt update && apt install -y ansible
fi

echo "[2/5] Пересоздаем тестовые Docker-контейнеры (node1 и node2)..."
docker rm -f node1 node2 2>/dev/null || true

docker run -d --name node1 --privileged --cgroupns=host \
  -v /sys/fs/cgroup:/sys/fs/cgroup:rw \
  geerlingguy/docker-ubuntu2004-ansible:latest

docker run -d --name node2 --privileged --cgroupns=host \
  -v /sys/fs/cgroup:/sys/fs/cgroup:rw \
  geerlingguy/docker-ubuntu2004-ansible:latest

echo "[3/5] Создаем inventory.ini..."
cat << 'EOF' > inventory.ini
[webservers]
node1 ansible_connection=docker
node2 ansible_connection=docker
EOF

echo "[4/5] Создаем playbook.yml..."
cat << 'EOF' > playbook.yml
---
- name: Multi-Node Fault-Tolerant Deployment
  hosts: webservers
  become: true

  vars:
    staging_dir: "/tmp/web_staging"
    app_dir: "/var/www/html"

  tasks:
    - name: Main Deployment Block (Try)
      block:
        - name: Create temporary staging directory
          file:
            path: "{{ staging_dir }}"
            state: directory

        - name: Staging deployment artifact
          copy:
            content: "<h1>Version 2.0 - Multi-Node Production</h1>"
            dest: "{{ staging_dir }}/index.html"

        - name: Ensure application directory exists
          file:
            path: "{{ app_dir }}"
            state: directory

        - name: Deploy artifact to application directory
          copy:
            src: "{{ staging_dir }}/index.html"
            dest: "{{ app_dir }}/index.html"
            remote_src: true

        - name: Confirm successful deployment
          debug:
            msg: "{{ inventory_hostname }} deployed successfully!"

      rescue:
        - name: CRITICAL ERROR - Triggering Automated Rollback
          debug:
            msg: "{{ inventory_hostname }} failed! Rolling back..."

        - name: Deploy emergency maintenance landing page
          copy:
            content: "<h1 style='color:red;'>System Under Emergency Maintenance</h1>"
            dest: "{{ app_dir }}/index.html"

      always:
        - name: CLEANUP - Remove temporary staging directory
          file:
            path: "{{ staging_dir }}"
            state: absent
EOF

echo "[5/5] Проверяем связь через пинг и запускаем плейбук..."
ansible -i inventory.ini webservers -m ping

echo "Запуск плейбука на двух нодах..."
ansible-playbook -i inventory.ini playbook.yml
OUTER_EOF

chmod +x setup_multi_node_docker.sh
./setup_multi_node_docker.sh