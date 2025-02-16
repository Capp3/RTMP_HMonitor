# RTMP_HMonitor

## Get Debian Ready

Install basic dependencies

```sh
apt update && \
apt upgrade -y \
apt-transport-https \
ca-certificates \
curl \
gnupg-agent \
software-properties-common \
git \
build-essential \
python3-dev \
python3-venv \
python3-pip \
x264 \
ffmpeg
```

## Install Docker for support services

Start be cleaning for docker

```sh
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

Add docker pgp keys

```sh
# Add Docker's official GPG key:
sudo apt-get update && \
sudo apt-get install ca-certificates curl && \
sudo install -m 0755 -d /etc/apt/keyrings && \
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && \
sudo apt-get update
```

Install Docker

```sh
 sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Add user to Docker group

```sh
sudo usermod -a -G docker $USER
```

Test Docker

```sh
sudo docker run hello-world
```

Support services can then be started

```sh
docker compose -f docker/docker-compose.yml up -d
```
