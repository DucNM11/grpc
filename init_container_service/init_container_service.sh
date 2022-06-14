#!/usr/bin/env bash

# Initializing start-up docker service to create a based VM image for ease of scaling out
sudo mv init_container.sh /usr/sbin/
sudo chmod 664 /usr/sbin/init_container.sh

sudo chmod 664 init_container.service
sudo mv init_container.service /etc/systemd/system/

sudo systemctl enable init_container
