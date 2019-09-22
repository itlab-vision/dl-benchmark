#!/bin/bash

echo "Update components"
#apt-get update

if [[ -z "$(ls /etc/ | grep vsftpd.conf)" ]]
then
    echo "Install/Update FTP-server"
    apt-get install vsftpd
    systemctl start vsftpd
    systemctl enable vsftpd
    cat ftp_server_settigs.txt > /etc/vsftpd.conf
fi

cd ~/Downloads/ 
wget $1 

arch_name="$(ls | grep ".tgz")"
tar -xvzf $arch_name
cd "$(basename $arch_name .tgz)"