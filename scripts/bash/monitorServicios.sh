#!/bin/bash

declare -a servicios=("apache2" "sshd" "postfix" "dovecot" "mariadb" "quotaon")
for servicio in "${servicios[@]}"
do
	estado=$(systemctl is-active $servicio)
	if [[ "$estado" == "active" ]]; then
    	#el servicio esta activo
    	echo 1 > /var/www/html/estado/$servicio
	else
    	echo 0 > /var/www/html/estado/$servicio
    	#el servicio esta inactivo
	fi
done

