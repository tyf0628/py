#!/bin/bash
dir=/usr/local/zabbix/share/zabbix/externalscripts/cpu
mkdir -p $dir/$1
cat /usr/local/zabbix/share/zabbix/externalscripts/cpu_temp.sql | sed -e "s/hostname_ip/$1/g" > $dir/$1/cpu_avg_new.sql
mysql --defaults-extra-file=/etc/no_warning_mysql.cnf < $dir/$1/cpu_avg_new.sql | awk '{ sum += $4; } END {print sum/(NR-1)}'

