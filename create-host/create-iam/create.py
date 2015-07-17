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
            hostname = lines[loop].split()[0].strip().upper().split(".")[0]
            address = lines[loop].split()[1].strip()
            filename = hostname + ".cfg"
            f = open("%s/%s" % (dir, filename), 'w')
            f.write("""define host {
    use          htpl_app_iam_win-server-toa
    host_name    %s
    address      %s
}""" % (hostname, address) + "\n")
