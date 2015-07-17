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


def delblankline(infile, outfile):
    """Delete blank line of infile"""
    infp = open(infile, 'r')
    outfp = open(outfile, 'w')
    lines = infp.readlines()
    for l in lines:
        if l.split():
            outfp.writelines(l)
    infp.close()
    outfp.close()

cur = os.getcwd()
filenames = ["%s/as" % cur, "%s/us" % cur, "%s/eu" % cur]
dir = "/home/chengca/faurecia-nagios-configuration/hosts"

if __name__ == "__main__":
    for file in filenames:
        resfile = cur + "/%sres" % os.path.basename(file)
        delblankline(file, resfile)

        f = open(resfile, 'r')
        lines = f.readlines()

        for loop in range(0, int("%d" % len(lines)), 2):
            hostname = lines[loop].split(":")[1].strip().upper().split(".")[0]
            filename = hostname + ".cfg"
            address = lines[loop+1].split(":")[1].strip()
            f = open("%s/%s" % (dir, filename), 'w')
            f.write("""define host {
    use          ohtpl_area_%s,\\
                 htpl_app_ad_ctl-2012
    host_name    %s
    address      %s
}""" % (os.path.basename(file), hostname, address) + "\n")
