# Install libvirt
# sudo pacman -S virt-manager virt-viewer
# sudo systemctl start libvirtd.service
# sudo systemctl start virtlogd.service
# sudo systemctl enable libvirtd.service

# curl -OL https://dl-cdn.alpinelinux.org/alpine/v3.18/releases/x86_64/alpine-standard-3.18.2-x86_64.iso
curl -OL https://dl-cdn.alpinelinux.org/alpine/v3.18/releases/x86_64/alpine-virt-3.18.2-x86_64.iso

sudo virsh net-start default

sudo virt-install  \
    --name exeter-gateway-lite \
    --memory 512 \
    --vcpus=1,maxvcpus=2 \
    --cpu host \
    --cdrom ./alpine-virt-3.18.2-x86_64.iso \
    --disk size=0.5,format=qcow2 \
    --network network=default \
    --virt-type kvm \
    --noautoconsole

sudo virsh console exeter-gateway-lite

# install manually, urgh
# Notes:
# login: root
# password [none]

## Partition disk
# fdisk /dev/vda
# n p 1 [default] +100M
# t ef
# a 1
# n p 2 [default] [default]
# w

# setup-alpine
# keyboard: gb
# variant: gb
# hostname: exeter-gateway
# interface: [eth0]
## Check output of `ip addr list` on host and pich something in /24 of virbr0 address
# ip: 192.168.122.100/24
# gateway: 192.168.122.1
# manual network config: n
# dns domain name: exeter-gateway
# dns domain server: 192.168.122.1
# root password: set one!
# timezone: Europe/London
# proxy: [none]

# user:
# password:
# ssh-key:
# ssh server: dropbear

# disk: vda
# use: data
# erase: n!!!

## Manual steps:
# mkfs.ext4 /dev/vda2
# mkfs.vfat /dev/vda1
# setup-ntp busybox

# apk add syslinux
# mount /dev/vda1 /mnt -t vfat
# setup-bootable /media/cdrom /mnt
# extlinux --install /mnt/boot/syslinux
# dd bs=440 count=1 conv=notrunc if=/usr/share/syslinux/mbr.bin of=/dev/vda

# mkdir /media/vda2
# mount /dev/vda2 /media/vda2
# setup-lbu
# vi /etc/apk/repositories
## Uncomment community mirror
# setup-apkcache
# lbu commit
# poweroff


