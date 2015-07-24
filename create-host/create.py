#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: create.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Mon 20 Jul 2015 10:25:10 AM EDT
######################################################################
# Description:
######################################################################

import argparse
import os

parser = argparse.ArgumentParser(description="Create new hosts in nagios.")
parser.add_argument("-l", "--location",
                    dest="location",
                    required=False,
                    help="The area of the host, eg: ohtpl_area_XX.")
parser.add_argument("-e", "--environment",
                    dest="environment",
                    required=False,
                    help="The environment of the host, eg: ohtpl_env_XX.")
parser.add_argument("-p", "--parents",
                    dest="parents",
                    required=False,
                    help="The parents of the host, eg: CLUSTER_BIS6_US.")
parser.add_argument("-a", "--applications",
                    dest="applications",
                    required=False,
                    help="The application of the host, eg: bhtpl/htpl_app_XX.")
parser.add_argument("-n", "--name",
                    dest="name",
                    required=False,
                    help="The hostname of the host, eg: PLWLBVMW0001, lower \
                    case or upper case is ok.")
parser.add_argument("-i", "--ip",
                    dest="ip",
                    required=False,
                    help="The ip or dns of the host, eg: \
                    plwlbvmw0001.wlb.pl.corp or 10.135.17.116.")
parser.add_argument("-m", "--mode",
                    dest="mode",
                    required=True,
                    help="If mode=0 use dns, mode=1 use ip.")
parser.add_argument("-f", "--files",
                    action="append",
                    dest="files",
                    help="If specify the file, read hostname ip and templates \
                    from this file.Just the name without suffix. \
                    The default file is <hosts.txt>. \
                    And the default templates file is <hosts.cfg>.")
args = parser.parse_args()

cur = os.getcwd()
home = os.environ["HOME"]
g_dir = "%s/faurecia-nagios-configuration/hosts" % home


def main():
    # Just use the file not the command line options.
    if args.files:
        for loop in range(0, len(args.files)):
            print "<<<<<<<<<<<<>>>>>>>>>>>>>"
            print "files: %s" % args.files
            filename = args.files[loop]
            print "filename: %s" % filename
            file = "%s/%s.txt" % (cur, filename)
            templates = "%s/%s.cfg" % (cur, filename)
            print "file: %s" % file
            print "templates: %s" % templates
            f = open(file, "r")
            lines = f.readlines()
            for loo in range(0, int("%d" % len(lines))):
                print "+++++++++++++++++++++++++++"
                print "line: %s" % lines[loo]
                hostname = lines[loo].split()[0].split(".")[0].strip().upper()
                address = lines[loo].split()[int(args.mode)].lower()
                hostfile = "%s/%s.cfg" % (g_dir, hostname)
                print "hostname: %s" % hostname
                print "address: %s" % address
                print "hostfile: %s" % hostfile
                if os.path.isfile(hostfile):
                    print ">>>>file exist<<<<<"
                fw = open(hostfile, "w")
                fr = open(templates, "r")
                rlines = fr.readlines()
                rlines.insert(1, "    host_name  %s\n" % hostname)
                rlines.insert(2, "    address    %s\n" % address)
                for line in rlines:
                    fw.write(line)
                fr.close()
                fw.close()
            f.close()

    # Use the command line options not the file.
    else:
        print ">>>This function is not online<<<\n"

if __name__ == "__main__":
    main()
