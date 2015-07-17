#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: create.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Thu 04 Jun 2015 03:04:42 PM CST
######################################################################
# Description:
######################################################################

import os


cur = os.getcwd()
file = "%s/hosts.txt" % cur
dir = "/home/chengca/faurecia-nagios-configuration/hosts"

if __name__ == "__main__":
        f = open(file, 'r')
        lines = f.readlines()

        for loop in range(0, int("%d" % len(lines)), 1):
            hostname1 = lines[loop].split()[0].strip().upper().split(".")[0]
            address1 = lines[loop].split()[1].strip()
            print "hostname1: %s, address1: %s" % (hostname1, address1)
            filename1 = hostname1 + ".cfg"
            f = open("%s/%s" % (dir, filename1), 'w')
            f.write("""define host {
    use          ohtpl_sys_vmware_us_nandcvcr0001,\\
                 bhtpl_sys_mii_esx-node
    host_name    %s
    address      %s
}""" % (hostname1, address1) + "\n")

            hostname2 = lines[loop].split()[2].strip().upper().split(".")[0]
            address2 = lines[loop].split()[3].strip()
            print "hostname2: %s, address2: %s" % (hostname2, address2)
            filename2 = hostname2 + ".cfg"
            f = open("%s/%s" % (dir, filename1), 'w')
            f.write("""define host {
    use          ohtpl_sys_vmware_us_nandcvcr0001,\\
                 bhtpl_sys_mii_esx-node
    host_name    %s
    address      %s
}""" % (hostname2, address2) + "\n")
