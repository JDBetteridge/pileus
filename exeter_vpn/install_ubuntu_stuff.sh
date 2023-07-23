#!/bin/bash
apt-get update
apt-get -y dist-upgrade
DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata
apt-get -y install curl libtdb1 network-manager

# TODO: Need to configure NetworkManager to use static IP

sudo systemctl start NetworkManager
sudo systemctl enable NetworkManager

curl -L https://h30326.www3.hpe.com/hpn/via_4.2.0.2105106-deb_amd64.deb?merchantId=ASP_DROPBOX -o via.deb

dpkg -i via.deb

rm -rf /var/lib/apt/lists/*

# Now setup via with `./setup_via_client.sh`
