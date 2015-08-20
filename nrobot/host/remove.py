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
import sys
import argparse

parser = argparse.ArgumentParser(description="This script used for remove \
                                 host from nagios.")
parser.add_argument("-P", "--path",
                    dest="path",
                    default="/home/chengca/faurecia-nagios-configuration",
                    required=False,
                    help="The path of faurecia-nagios-configuration.")
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
home = os.getenv("HOME")
path = "faurecia-nagios-configuration"
g_dir = "%s/hosts" % args.path
comment = "#########################################"


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
    elif args.name:
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
        print "Please specify the options. And try again."
        sys.exit()

if __name__ == "__main__":
    main()
