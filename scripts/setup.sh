#!/bin/bash
# Server setup script: packages, Docker, deploy user, aliases
set -e

export DEBIAN_FRONTEND=noninteractive

echo "== 1/4 Updating packages =="
sudo apt-get update
sudo -E apt-get upgrade -y

echo "== 2/4 Installing required packages =="
sudo -E apt-get install -y git curl nginx docker.io docker-compose-v2 certbot python3-certbot-nginx
sudo systemctl enable --now docker
sudo -E apt-get install -y git curl nginx docker.io docker-compose-v2 certbot python3-certbot-nginx supervisor

echo "== 3/4 Creating deploy user =="
if ! id deploy >/dev/null 2>&1; then
    sudo adduser --disabled-password --gecos "" deploy
fi
sudo usermod -aG docker deploy
sudo usermod -aG docker ubuntu

echo "== 4/4 Adding aliases =="
if ! grep -q "# devops-aliases" ~/.bashrc; then
    cat >> ~/.bashrc << 'EOF'
# devops-aliases
alias ll='ls -alF'
alias dps='docker ps'
alias dlogs='docker compose logs -f'
alias update='sudo apt update && sudo apt upgrade -y'
EOF
fi

echo "Setup complete! Run 'exit' and reconnect so the docker group takes effect."
