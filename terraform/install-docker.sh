#!/bin/bash

if ! command -v docker version &> /dev/null
then
  sudo apt-get -y update
  sudo apt-get -y install \
      ca-certificates \
      curl \
      gnupg \
      lsb-release

  sudo mkdir -p /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  sudo apt-get -y update
  sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin

  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.0/docker-compose-$(uname -s)-$(uname -m)"  -o /usr/local/bin/docker-compose
  sudo mv /usr/local/bin/docker-compose /usr/bin/docker-compose
  sudo chmod +x /usr/bin/docker-compose

  sudo usermod -aG docker ubuntu

  echo "Install completed"
else
  sudo docker-compose stop
fi
