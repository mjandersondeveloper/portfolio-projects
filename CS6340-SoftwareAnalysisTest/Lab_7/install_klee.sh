#!/bin/sh

# CS6340 Course VM update Script to install Docker and KLEE docker image.
# Also contains some handy commands, commented out so they don't run.
# Author: Michael D. Brown
# References: KLEE documentation (klee.github.io/docker)

# Disable EOL repositories
# sudo sed '/^deb/s/^/## /' /etc/apt/sources.list > /etc/apt/sources.list

# Add EOL Zesty release repositories
# sudo echo "deb http://old-releases.ubuntu.com/ubuntu/ zesty main restricted universe multiverse" >> /etc/apt/sources.list
# sudo echo "deb http://old-releases.ubuntu.com/ubuntu/ zesty-updates main restricted universe multiverse" >> /etc/apt/sources.list
# sudo echo "deb http://old-releases.ubuntu.com/ubuntu/ zesty-security main restricted universe multiverse" >> /etc/apt/sources.list

# Install Docker
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# sudo apt-key fingerprint 0EBFCD88
# sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# sudo apt-get update
# sudo apt-get -y install docker-ce

# Test Docker Install
sudo docker run hello-world

# Install KLEE Docker Image
sudo docker pull klee/klee:1.4.0


# klee (lab folder) Handy Commands

# To run the KLEE Docker image for the first time with the klee folder mapped
# sudo docker run -v /home/cs6340/klee/:/home/klee/klee -ti --name=klee_container --ulimit='stack=-1:-1' klee/klee

# Check that KLEE container is still runnning
# sudo docker ps -a

# To re-run the KLEE Docker image after exiting
# sudo docker start -ai klee_container

# Remove a container (to start over from scratch)
# sudo docker rm klee_container
