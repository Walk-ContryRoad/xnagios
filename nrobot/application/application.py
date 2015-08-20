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
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        self.cur = os.getcwd() + "/application"
        self.hostgroup = "%s/hostgroup.cfg" % self.cur
        self.template = "%s/template.cfg" % self.cur
        self.h_dir = "%s/hostgroups/app/" % self.args.path
        self.t_dir = "%s/templates/hosts/app/" % self.args.path
        if self.args.application:
            self.application = self.args.application
            self.hostgroupfile = self.h_dir + self.application + ".cfg"
            self.templatefile = self.t_dir + self.application + ".cfg"

        if self.__class__.__name__ == "Application":
            self.logger.debug("==== END DEBUG ====")

    def define_options(self):
        super(Application, self).define_options()
        self.parser.add_argument("-a", "--application",
                                 dest="application",
                                 required=False,
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

    def create_hostgroup(self):
        if os.path.isfile(self.hostgroupfile):
            self.already_exist(self.hostgroupfile)
        else:
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

    def create_template(self):
        if os.path.isfile(self.templatefile):
            self.already_exist(self.templatefile)
        else:
            ftr = open(self.template, "r")
            lines = ftr.readlines()
            ftw = open(self.templatefile, "a")
            for loop in range(0, len(lines)):
                line = lines[loop]
                if 0 <= loop <= 13:
                    if loop == 7:
                        if self.args.domain:
                            ftw.write(line % self.args.domain)
                        else:
                            pass
                    elif "%s" in line and loop != 7:
                        ftw.write(line % self.application)
                    else:
                        ftw.write(line)
            for loop in range(0, len(self.args.system)):
                system = self.args.system[loop]
                for loo in range(0, len(lines)):
                    line = lines[loo]
                    if 14 <= loo <= 22:
                        if loo == 14 or loo == 16 or loo == 19:
                            ftw.write(line % (self.application, system))
                        elif loo == 17:
                            ftw.write(line % self.application)
                        elif loo == 18:
                            ftw.write(line % system)
                        else:
                            ftw.write(line)
            for loop in range(0, len(lines)):
                line = lines[loop]
                if 23 <= loop <= 25:
                    ftw.write(line)
            for loop in range(0, len(self.args.system)):
                system = self.args.system[loop]
                for loo in range(0, len(lines)):
                    line = lines[loo]
                    if 26 <= loo <= 33:
                        if "%s" in line:
                            ftw.write(line % (self.application, system))
                        else:
                            ftw.write(line)

    def delete_hostgroup(self):
        if not os.path.isfile(self.hostgroupfile):
            self.not_exist(self.hostgroupfile)
        else:
            try:
                os.remove(self.hostgroupfile)
            except Exception as e:
                self.error("Error delete_hostgroup: %s" % e)

    def delete_template(self):
        if not os.path.isfile(self.templatefile):
            self.not_exist(self.templatefile)
        else:
            try:
                os.remove(self.templatefile)
            except Exception as e:
                self.error("Error delete_template: %s" % e)
