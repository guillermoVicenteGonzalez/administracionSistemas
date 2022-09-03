#!/bin/bash


comando=sshd
estado=$(systemctl is-active sshd)
if [[ "estado" == "active" ]]; then
    #el servicio esta activo
    echo 1 > /var/www/html/estado/$comando
else
    echo "Strings are not equal."
fi

