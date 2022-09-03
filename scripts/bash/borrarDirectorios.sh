#!/bin/bash

cd /home
cut -d: -f1 /etc/passwd > /var/pecera/usuarios.txt;
ls -l /home | awk '{print $9'} > /var/pecera/carpetas.txt


while read line;
do
	array+=$line;
	#a=$(grep -i line /var/pecera/usuarios.txt)
	#if [ -z "$a" ]; then echo "NULL"; else echo "Not NULL"; fi
done < /var/pecera/carpetas.txt

for value in "${array[@]}"
do
	echo $value
done

#a=$(grep -i "^chingu" /etc/passwd)
#if [ -z "$a" ]; then echo "NULL"; else echo "Not NULL"; fi