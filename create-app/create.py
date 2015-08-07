#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: create.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Thu 16 Jul 2015 05:03:18 AM EDT
######################################################################
# Description:
######################################################################

import os
import sys
import argparse
import commands

parser = argparse.ArgumentParser(description="This script used for create a \
                                 new application in nagios.")
parser.add_argument("-p", "--path",
                    dest="path",
                    required=False,
                    help="The path of faurecia-nagios-configuration.")
parser.add_argument("-a", "--application",
                    dest="application",
                    required=True,
                    help="New application name, type is a string.")
parser.add_argument("-d", "--domain",
                    dest="domain",
                    required=False,
                    help="Domain name, if requestor no ask it's null. \
                    eg: cws or eit.")
parser.add_argument("-s", "--system",
                    action="append",
                    dest="system",
                    required=True,
                    help="What system used in this new applicaion. \
                    eg: win aix solaris linux as400 bladecenter \
                    and hyper-v. Multity system use -s system1 -s system2 ...")
args = parser.parse_args()

cur = os.getcwd()
home = os.getenv("HOME")
path = "faurecia-nagios-configuration"
if args.path:
    g_dir = args.path
else:
    output = commands.getoutput("sudo find %s -name %s" % (home, path))
    if len(output.split()) != 1:
        print """%s
        More than one path.
        Please use -P to specify the path.""" % output
        sys.exit()
    else:
        g_dir = output
t_dir = "%s/templates/hosts/app" % (g_dir)
h_dir = "%s/hostgroups/app" % (g_dir)


def main():
    app = args.application
    sys = args.system

    # Create hostgroups.
    fh = open("%s/%s.cfg" % (h_dir, app), "w")
    fh.write("""define hostgroup {
    hostgroup_name    app_%s
    alias             Application - %s
}""" % (app, app.upper()) + "\n")

    # Create template.
    ft = open("%s/%s.cfg" % (t_dir, app), "a")

    if args.domain:
        domain = args.domain
        ft.write("""# Application template for %s
#
define host {
    name          bhtpl_app_%s
    use           bhtpl_app_generic
    hostgroups    +app_%s,\\
                  domain_%s
    _PROC_DIR     %s
    register      0
}

#------------------------------------------------------------------------
# Templates used to setup OS used for the application
#------------------------------------------------------------------------
""" % (app, app, app, domain, app) + "\n")

    else:
        ft.write("""# Application template for %s
#
define host {
    name          bhtpl_app_%s
    use           bhtpl_app_generic
    hostgroups    +app_%s
    _PROC_DIR     %s
    register      0
}

#------------------------------------------------------------------------
# Templates used to setup OS used for the application
#------------------------------------------------------------------------
""" % (app, app, app, app) + "\n")

    # Add system.
    for loop in range(0, len(args.system)):
        sys = args.system[loop]
        ft.write("""# Base for %s %s servers
define host {
    name        bhtpl_app_%s_%s
    use         bhtpl_app_%s,\\
                htpl_sys_%s_server
    alias       %s - Standard %s Server
    register    0
}""" % (app, sys, app, sys, app, sys, app.upper(), sys) + "\n" + "\n")

if __name__ == "__main__":
    main()
