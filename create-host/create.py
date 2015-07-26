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
                    help="The environment of host, eg: ohtpl_env_XX.")
parser.add_argument("-p", "--parents",
                    dest="parents",
                    required=False,
                    help="The parents of host, eg: CLUSTER_BIS6_US.")
parser.add_argument("-a", "--applications",
                    dest="applications",
                    required=False,
                    help="The application of host, eg: htpl_app_XX.")
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
parser.add_argument("-s", "--services",
                    action="append",
                    dest="services",
                    required=False,
                    help="The services of the host, \
                    eg: inc_app_XXX. Use this like -s ex1 -s ex2....")
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
home = os.environ["HOME"]
g_dir = "%s/faurecia-nagios-configuration/hosts" % home
comment = "###########################################"


def usage():
    print("This is command line mode, \
          arguments for -a -n and -i is necessary.")
    print("""-l, --location,
              The area of the host, eg: ohtpl_area_XX.""")
    print("""-e, --environment,
              The environment of host, eg: ohtpl_env_XX.""")
    print("""-p, --parents,
              The parents of host, eg: CLUSTER_BIS6_US.""")
    print("""-a, --applications,
              The application of host, eg: htpl_app_XX.""")
    print("""-n, --name,
              The hostname of host, \
              eg: PLWLBVMW0001, lower case or upper case is ok.""")
    print("""-i, --ip,
              The ip or dns of the host, \
              eg: plwlbvmw0001.wlb.pl.corp or 10.135.17.116.""")
    print("""-s, --services,
              The services of the host, eg: inc_app_XXX.""")


def main():
    # Just use the file not the command line options.
    if args.files:
        for loop in range(0, len(args.files)):
            filename = args.files[loop]
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
                    print "# %s exist, next one. #" % hostfile
                    print "%s%s\n" % (comment, comment)
                    continue
                # If a new host, create it.
                else:
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
        if args.applications and args.name and args.ip:
            hostname = args.name.upper()
            address = args.ip.lower()
            hostfile = "%s/%s.cfg" % (g_dir, hostname)
            if os.path.isfile(hostfile):
                print "\n%s%s" % (comment, comment)
                print "# %s exist, next one. #" % hostfile
                print "%s%s\n" % (comment, comment)
            else:
                f = open(hostfile, "a")
                f.write("""def host {
    host_name  %s
    address    %s\n""" % (hostname, address))
                if args.location and args.environment:
                    f.write("""    use        %s,\\
               %s,\\
               %s""" % (args.location,
                        args.environment,
                        args.applications))
                elif args.location and (not args.environment):
                    f.write("""    use        %s,\\
               %s""" % (args.location,
                        args.applications))
                elif args.environment and (not args.location):
                    f.write("""    use        %s,\\
               %s""" % (args.environment,
                        args.applications))
                else:
                    f.write("    use        %s" % (args.applications))
                if args.parents:
                    f.write("\n    parents    %s\n" % args.parents)
                if args.services:
                    if len(args.services) == 1:
                        f.write("    hostgroups +%s" % args.services[0])
                    else:
                        for lo in range(0, len(args.services)):
                            if lo == 0:
                                f.write("    hostgroups +%s,\\\n" %
                                        args.services[lo])
                            elif lo == len(args.services) - 1:
                                f.write("               %s" %
                                        args.services[lo])
                            else:
                                f.write("               %s,\\\n" %
                                        args.services[lo])
                f.write("\n}\n")
                f.close()
        else:
            usage()

if __name__ == "__main__":
    main()
