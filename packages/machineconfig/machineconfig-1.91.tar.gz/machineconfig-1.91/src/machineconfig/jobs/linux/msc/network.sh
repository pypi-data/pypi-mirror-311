
# https://askubuntu.com/questions/972215/a-start-job-is-running-for-wait-for-network-to-be-configured-ubuntu-server-17-1
# This is the network config written by 'subiquity'
# network:
#   ethernets:
#     enp0s31f6:
#       dhcp4: true
#       optional: true
#   version: 2


sudo sed -i 's/dhcp4: true/dhcp4: true\n      optional: true/g' /etc/netplan/00-installer-config.yaml

# see sed and awk
# https://unix.stackexchange.com/questions/642578/command-line-for-editing-a-configuration-file-value-without-an-interactive-edito
# file format
# https://askubuntu.com/questions/304999/not-able-to-execute-a-sh-file-bin-bashm-bad-interpreter
# plocate:
# https://unix.stackexchange.com/questions/113670/can-i-just-disable-updatedb/113681#113681
# https://askubuntu.com/questions/1251484/why-does-it-take-so-much-time-to-initialize-mlocate-database

