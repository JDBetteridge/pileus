#!/bin/bash
sudo via-vpn-srv
sleep 2s
via-cli session start
via-cli vpn connect

# !?
sudo ifconfig via_vpn mtu 1200 up
