#!/bin/bash

rsync -ravzh /home/ /backups/home
rsync -ravzh /root/ /backups/root
rsync -ravzh /var/lib/mysql/ /backups/mysql/
rsync -ravzh /var/www/html /backups/html