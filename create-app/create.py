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
import argparse


cur = os.getcwd()
home = os.environ["HOME"]
g_dir = "faurecia-nagios-configuration"
t_dir = "%s/%s/templates/hosts/app" % (home, g_dir)
h_dir = "%s/%s/hostgroups/app" % (home, g_dir)


parser = argparse.ArgumentParser(description="This script used for create a \
                                 new application in nagios.")
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
