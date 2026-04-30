#cloud-config
package_update: true
package_upgrade: true

packages:
  - apt-transport-https
  - ca-certificates
  - curl
  - git

runcmd:
  # Install Docker (for building images on the node)
  - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker.gpg
  - echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu noble stable" > /etc/apt/sources.list.d/docker.list
  - apt-get update
  - apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker ${admin_username}

  # Clone repo
  - git clone ${repo_url} /opt/app
  - cp /opt/app/.env.example /opt/app/.env

  # Install k3s
  - curl -sfL https://get.k3s.io | sh -
  - systemctl enable k3s

  # Build images and import into k3s containerd
  - docker build -t analytics/data_load:v1 -f /opt/app/src/data_load/Dockerfile /opt/app
  - docker save analytics/data_load:v1 | k3s ctr images import -
  - docker build -t analytics/data_quality_analysis:v1 -f /opt/app/src/data_quality_analysis/Dockerfile /opt/app
  - docker save analytics/data_quality_analysis:v1 | k3s ctr images import -
  - docker build -t analytics/data_research:v1 -f /opt/app/src/data_research/Dockerfile /opt/app
  - docker save analytics/data_research:v1 | k3s ctr images import -
  - docker build -t analytics/visualization:v1 -f /opt/app/src/visualization/Dockerfile /opt/app
  - docker save analytics/visualization:v1 | k3s ctr images import -
  - docker build -t analytics/web:v1 -f /opt/app/web/Dockerfile /opt/app
  - docker save analytics/web:v1 | k3s ctr images import -

  # Install Argo CD
  - kubectl create namespace argocd --kubeconfig /etc/rancher/k3s/k3s.yaml
  - kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --kubeconfig /etc/rancher/k3s/k3s.yaml

  # Expose Argo CD via NodePort
  - kubectl patch svc argocd-server -n argocd -p '{"spec":{"type":"NodePort","ports":[{"port":443,"targetPort":8080,"nodePort":30443}]}}' --kubeconfig /etc/rancher/k3s/k3s.yaml
