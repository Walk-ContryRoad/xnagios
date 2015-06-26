######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: create_host.sh
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: 2015年05月20日 星期三 11时04分12秒
######################################################################
# Description:                                                        
######################################################################
#!/usr/bin/env bash

#this script used for create a lot of host configuration file for nagios.

HOST=$HOME/hosts.txt
DIR=$HOME/GIT/faurecia-nagios-configuration/hosts

for LINE in `cat $HOST`
do
	address=`echo $LINE | awk '{print tolower($1)}'`
    hostname=`echo $LINE | awk '{print $1}' | awk -F'.' '{print toupper($1)}'`

	if [[ $hostname -ne 10 ]]
	then
        if [[ -e $DIR/${hostname}.cfg ]]
        then
            echo ">>$DIR/${hostname}.cfg already exist.<<"
        else
		    echo "define host {
	use        ohtpl_sys_vmware_eu_euedcvcr0001,\\
               bhtpl_sys_mii_esx-node
    host_name   ${hostname}
    address    ${address}
}" > $DIR/${hostname}.cfg
        fi
    fi
done

exit
