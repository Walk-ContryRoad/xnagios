#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: remove.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Wed 15 Jul 2015 10:17:28 PM EDT
######################################################################
# Description:
######################################################################

import os
import argparse

parser = argparse.ArgumentParser(description="This script used for remove \
                                 host from nagios.")
parser.add_argument("-n", "--name",
                    action="append",
                    dest="name",
                    required=False,
                    help="This is the hostname you want ot remove.")
parser.add_argument("-f", "--file",
                    dest="file",
                    required=False,
                    help="This is the hostname file you want to remove.")
args = parser.parse_args()

cur = os.getcwd()
home = os.environ["HOME"]
g_dir = "%s/faurecia-nagios-configuration/hosts" % home
comment = "#########################################"


def usage():
    print "Use command line option -n to remove host from nagios."
    print "-n hostname1 -n hostname2 ...."


def main():
    if args.file:
        f = open(args.file, "r")
        lines = f.readlines()
        for line in lines:
            if line:
                hostname = line.split()[0].split(".")[0].strip().upper()
                hostfile = "%s/%s.cfg" % (g_dir, hostname)
                if not os.path.isfile(hostfile):
                    print "%s%s" % (comment, comment)
                    print "# %s not exist. #" % hostfile
                    print "%s%s\n" % (comment, comment)
                else:
                    os.remove(hostfile)
    else:
        if args.name:
            for loop in range(0, len(args.name)):
                hostname = args.name[loop].split(".")[0].strip().upper()
                hostfile = "%s/%s.cfg" % (g_dir, hostname)
                if not os.path.isfile(hostfile):
                    print "%s%s" % (comment, comment)
                    print "# %s not exist. #" % hostfile
                    print "%s%s\n" % (comment, comment)
                else:
                    os.remove(hostfile)
        else:
            usage()

if __name__ == "__main__":
    main()
