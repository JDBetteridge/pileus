###!/bin/bash

# These are notes, not a script

sudo virsh start exeter-gateway-lite
ssh 192.168.122.100 # or ssh exeter-gateway

# On the gateway
./start_via_vpn.sh
exit

ssh pileus
