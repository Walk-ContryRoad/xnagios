######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: gitdelete.sh
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: 2015年05月20日 星期三 13时55分40秒
######################################################################
# Description:                                                        
######################################################################
#!/usr/bin/env bash

#used for delete remote branch after weekly integration.

CUR=`pwd`
FILE=$CUR/gitdelete.txt
DES=$CUR/gitnum.txt
GIT=$HOME/faurecia-nagios-configuration
REMOTE=u/chengca/request

awk '{print $1}' $FILE | sed s/#// > $DES

for NUM in `cat $DES`
do
	cd $GIT
	git push -u origin :$REMOTE/$NUM
done

exit
