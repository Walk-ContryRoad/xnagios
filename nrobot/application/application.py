#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: application.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Thu 16 Jul 2015 05:03:18 AM EDT
######################################################################
# Description:
######################################################################

import os
from base import NagiosAuto


class Application(NagiosAuto):
    """Function for create new applicaion and remove application."""
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        self.cur = os.getcwd() + "/application"
        self.hostgroup = "%s/hostgroup.cfg" % self.cur
        self.template = "%s/template.cfg" % self.cur
        self.h_dir = "%s/hostgroups/app/" % self.args.path
        self.t_dir = "%s/templates/hosts/app/" % self.args.path
        self.hostgroupfile = self.h_dir + self.args.application + ".cfg"
        self.templatefile = self.t_dir + self.args.application + ".cfg"

        if self.__class__.__name__ == "Application":
            self.logger.debug("==== END DEBUG ====")

        self.logger.debug("leave application")

    def define_options(self):
        super(Application, self).define_options()
        self.parser.add_argument("-a", "--application",
                                 dest="application",
                                 required=True,
                                 help="New application name.")
        self.parser.add_argument("-d", "--domain",
                                 dest="domain",
                                 required=False,
                                 help="Domain name, eg: cws or eit.")
        self.parser.add_argument("-s", "--system",
                                 action="append",
                                 dest="system",
                                 required=False,
                                 help="System used in this new applicaion. \
                                 eg: win aix solaris linux as400 bladecenter \
                                 Multity system use -s system1 -s system2 ...")
        self.parser.add_argument("-S", "--service",
                                 action="append",
                                 dest="service",
                                 required=False,
                                 help="The common services in common roles.")

    def create_hostgroup(self):
        fhr = open(self.hostgroup, "r")
        lines = fhr.readlines()
        fhw = open(self.hostgroupfile, "w")
        for line in lines:
            if "%s" in line:
                fhw.write(line % self.args.application)
            else:
                fhw.write(line)
        fhr.close()
        fhw.close()

    def delete_hostgroup(self):
        if not os.path.isfile(self.hostgroupfile):
            self.not_exist(self.hostgroupfile)
        else:
            try:
                os.remove(self.hostgroupfile)
            except Exception as e:
                self.error("Error delete_hostgroup : %s" % e)
