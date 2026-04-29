#cloud-config
package_update: true
package_upgrade: true

packages:
  - docker.io
  - docker-compose-plugin
  - git

runcmd:
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker ${admin_username}
  - git clone ${repo_url} /opt/app
  - cd /opt/app && docker compose up -d
