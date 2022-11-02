#!/bin/bash       
username="emr_remote_db_backup"
ip_address="192.168.11.103"
password="lin@1088"

sshpass -p $password rsync -rav --progress /var/www/EMR-DB-BACKUP/ $username@$ip_address:/var/www/Remote-DB-BacksUps/test_dir/