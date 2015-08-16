#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: base.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Tue 11 Aug 2015 04:28:53 AM EDT
######################################################################
# Description:
######################################################################

import logging
import argparse
import sys
import os


class NagiosAuto(object):
    # Initialize a new class.
    def __init__(self, name=None, version='', description=''):
        # Init the logger.
        logging.basicConfig(format='[%(levelname)s] (%(module)s) %(message)s')
        self.logger = logging.getLogger("NagiosAuto")
        self.logger.setLevel(logging.INFO)

        # Init the basic information.
        self.name = os.path.basename(sys.argv[0]) if not name else name
        self.version = version
        self.description = description
        self.path = "/home/chengca/faurecia-nagios-configuration"

        # Init the arguments.
        self.__define_module_options()
        self.define_options()
        self.__parse_options()

        if self.args.debug:
            self.logger.setLevel(logging.DEBUG)

        self.logger.debug("==== BEGIN DEBUG ====")
        self.logger.debug("name: %s", self.name)
        self.logger.debug("version: %s", self.version)
        self.logger.debug("description: %s", self.description)

        if self.__class__.__name__ == "NagiosAuto":
            self.logger.debug("==== END DEBUG ====")

        self.logger.debug("leave base")

    def __define_module_options(self):
        self.parser = argparse.ArgumentParser(description=self.description)
        # Define the basic options here.
        self.parser.add_argument("--debug",
                                 action="store_true",
                                 dest="debug",
                                 help="Show debug information.")
        self.required_args = self.parser.add_argument_group("Subprocess.")

    def __parse_options(self):
        try:
            self.args = self.parser.parse_args()
        except Exception as e:
            self.error("Error __parse_options : %s" % e)

    def define_options(self):
        # This arguments for all function.
        self.required_args.add_argument("-P", "--path",
                                        dest="path",
                                        default="%s" % self.path,
                                        required=False,
                                        help="The path of \
                                        faurecia-nagios-configuration.")

    def error(self, msg):
        raise NagiosAutoError(msg)

    def warning(self, msg):
        raise NagiosAutoWarning(msg)

    def not_exist(self, msg):
        comment = "+++++++++++++++++++++++++++++++++++++++++++++++"
        print "%s%s" % (comment, comment)
        print "%s not exist." % msg
        print "%s%s" % (comment, comment)


class NagiosAutoError(Exception):
    def __init__(self, msg):
        print "Error - %s" % msg
        raise SystemExit(1)


class NagiosAutoWarning(Exception):
    def __init__(self, msg):
        print "Warning - %s" % msg
        raise SystemExit(2)
