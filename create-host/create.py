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
import sys

parser = argparse.ArgumentParser(description="Create new hosts in nagios.")
parser.add_argument("-P", "--path",
                    dest="path",
                    default="/home/chengca/faurecia-nagios-configuration",
                    required=False,
                    help="Use this specify the path of your git repo.")
parser.add_argument("-a", "--applications",
                    action="append",
                    dest="applications",
                    required=False,
                    help="The application of host, eg: htpl_app_XX. \
                    you can specify the area and environment.")
parser.add_argument("-n", "--name",
                    dest="name",
                    required=False,
                    help="The hostname of host, \
                    eg: PLWLBVMW0001, lower case or upper case is ok.")
parser.add_argument("-i", "--ip",
                    dest="ip",
                    required=False,
                    help="The ip or dns of the host, \
                    eg: plwlbvmw0001.wlb.pl.corp or 10.135.17.116.")
parser.add_argument("-p", "--parents",
                    dest="parents",
                    required=False,
                    help="The parents of host, eg: CLUSTER_BIS6_US.")
parser.add_argument("-s", "--services",
                    action="append",
                    dest="services",
                    required=False,
                    help="The services of the host, \
                    eg: inc_app_XXX. Use this like -s ex1 -s ex2....")
parser.add_argument("-d", "--delimiter",
                    dest="delimiter",
                    type=str,
                    default="@",
                    required=False,
                    help="This is the delimiter for extra arguments.")
parser.add_argument("-e", "--extra",
                    action="append",
                    dest="extra",
                    required=False,
                    help="Add the extra arguments. eg: -e arg1@val1 ")
parser.add_argument("-m", "--mode",
                    dest="mode",
                    required=False,
                    help="If mode=0 use dns, mode=1 use ip.")
parser.add_argument("-f", "--files",
                    action="append",
                    dest="files",
                    help="If specify the file, read hostname ip and templates \
                    from this file.Just the name without suffix. \
                    The default file is <hosts.txt>. \
                    And the default templates file is <hosts.cfg>. \
                    Use it like this -f file1 -f file2 ....")
args = parser.parse_args()

cur = os.getcwd()
home = os.getenv("HOME")
path = "faurecia-nagios-configuration"
g_dir = "%s/hosts" % args.path
comment = "###########################################"


def main():
    # Just use the file not the command line options.
    if args.files and args.mode:
        for loop in range(0, len(args.files)):
            filename = args.files[loop]
            print ">>> in %s <<<" % filename
            file = "%s/%s.txt" % (cur, filename)
            templates = "%s/%s.cfg" % (cur, filename)
            f = open(file, "r")
            lines = f.readlines()
            for loo in range(0, int("%d" % len(lines))):
                hostname = lines[loo].split()[0].split(".")[0].strip().upper()
                address = lines[loo].split()[int(args.mode)].lower()
                hostfile = "%s/%s.cfg" % (g_dir, hostname)
                # If file exist, jump to next one.
                if os.path.isfile(hostfile):
                    print "\n%s%s" % (comment, comment)
                    print "# %s exist, next one.#" % hostfile
                    print "%s%s\n" % (comment, comment)
                    continue
                # If a new host, create it.
                else:
                    fw = open(hostfile, "w")
                    fr = open(templates, "r")
                    rlines = fr.readlines()
                    rlines.insert(1, "    host_name            %s\n" %
                                  hostname)
                    rlines.insert(2, "    address              %s\n" % address)
                    for line in rlines:
                        fw.write(line)
                    fr.close()
                    fw.close()
            f.close()

    # Use the command line options not the file.
    elif args.applications and args.name and args.ip:
        hostname = args.name.upper()
        address = args.ip.lower()
        hostfile = "%s/%s.cfg" % (g_dir, hostname)
        if os.path.isfile(hostfile):
            print "\n%s%s" % (comment, comment)
            print "# %s exist, next one.#" % hostfile
            print "%s%s\n" % (comment, comment)
        else:
            f = open(hostfile, "a")
            f.write("""define host {
    host_name            %s
    address              %s\n""" % (hostname, address))
            if len(args.applications) == 1:
                f.write("    use                  %s\n" % args.applications[0])
            else:
                for loop in range(0, len(args.applications)):
                    if loop == 0:
                        f.write("    use                  %s,\\\n" %
                                args.applications[loop])
                    elif loop == len(args.applications) - 1:
                        f.write("                         %s\n" %
                                args.applications[loop])
                    else:
                        f.write("                         %s,\\\n" %
                                args.applications[loop])
            if args.parents:
                f.write("    parents              %s\n" % args.parents)
            if args.services:
                if len(args.services) == 1:
                            f.write("    hostgroups +         %s\n" %
                                    args.services[0])
                else:
                    for loop in range(0, len(args.services)):
                        if loop == 0:
                            f.write("    hostgroups           +%s,\\\n" %
                                    args.services[loop])
                        elif loop == len(args.services) - 1:
                            f.write("                         %s\n" %
                                    args.services[loop])
                        else:
                            f.write("                         %s,\\\n" %
                                    args.services[loop])
            if args.extra:
                for loop in range(0, len(args.extra)):
                    arg = args.extra[loop].split(args.delimiter)[0]
                    val = args.extra[loop].split(args.delimiter)[1]
                    space = (25 - 4 - len(arg)) * " "
                    f.write("    %s%s%s\n" % (arg, space, val))
            f.write("}\n")
            f.close()
    else:
        print "Please specify the arguments. And try again."
        sys.exit()

if __name__ == "__main__":
    main()
