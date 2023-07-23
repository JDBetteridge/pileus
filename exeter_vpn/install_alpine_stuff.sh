#!/bin/ash
apk update
apk upgrade
apk add curl networkmanager iptables tdb libxml2 dpkg libc6-compat gcompat dropbear-dbclient

# Link ssh to dbclient (for convenience)
ln -s /usr/bin/dbclient /usr/bin/ssh

# Link sudo to doas (similarly)
ln -s /usr/bin/doas /usr/bin/sudo

# Start and enable NetworkManaer
rc-service networkmanager start
rc-update add networkmanager default

# Start and enable iptables
/etc/init.d/iptables save
rc-service iptables start
rc-update add iptables

# Start and enable the tunnel device
modprobe tun
echo "tun" >> /etc/modules-load.d/tun.conf

# Download and install the via client
curl -L https://h30326.www3.hpe.com/hpn/via_4.5.0.2301032-deb_amd64.deb?merchantId=ASP_DROPBOX -o via.deb
# Force since this is not Debian/Ubuntu
# --force-all ?
# This step fails but gets "far enough" to work
dpkg -i --force-architecture --force-depends via.deb

# Now setup via with `ash setup_via_client.sh`

# Commit everything to Alpine local backup with:
lbu exclude /home/jack/exeter.cert /home/jack/via.deb
lbu add /usr/bin/ssh /usr/bin/sudo /usr/bin/*via*
lbu add /lib/security/*
lbu add /usr/lib/liban*
lbu add /usr/share/applications/via-ui.desktop
lbu add /usr/share/doc/via/*
lbu add /usr/share/gnome-vpn-properties/viavpn/*
lbu add /usr/share/icons/hicolor/**/apps/via.png /usr/share/pixmaps/via.png
lbu add /usr/share/via/*
