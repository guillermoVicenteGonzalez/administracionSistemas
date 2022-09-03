#!/bin/bas
#este script genera los datos para el admin todas las noches.

#uso de memoria.
free -m > /var/pecera/datos/free.txt	
#procesos y porcentaje de uso
sa -c > /var/pecera/datos/comandos.txt
#aqui se puede usar top?
top -n 1 -b> /var/pecera/datos/carga.txt


