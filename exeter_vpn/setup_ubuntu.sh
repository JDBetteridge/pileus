# Install libvirt
# sudo pacman -S virt-manager virt-viewer
# sudo systemctl start libvirtd.service
# sudo systemctl start virtlogd.service
# sudo systemctl enable libvirtd.service

curl -OL https://releases.ubuntu.com/22.04.2/ubuntu-22.04.2-live-server-amd64.iso

sudo virsh net-start default

sudo virt-install  \
    --name exeter-gateway \
    --memory 4096 \
    --vcpus=4,maxvcpus=8 \
    --cpu host \
    --cdrom ./ubuntu-22.04.2-live-server-amd64.iso \
    --disk size=4,format=qcow2 \
    --network network=default \
    --virt-type kvm \
    --noautoconsole

# install manually, urgh
# user1
# 57tMtbZvecNdiHjgkPXt
# ssh in
