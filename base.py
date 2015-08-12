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
import os
import sys


class NagiosAuto():
    # Initialize a new class.
    def __init__(self, name=None, version='', description=''):
        self.name = os.path.basename(sys.argv[0]) if not name else name
        self.version = version
        self.description = description

        self.parser = argparse.ArgumentParser(description=self.description)
        self.define_options()
        self.required_args = self.parser.add_argument_group("Subprocess.")
        self.options = self.parser.parse_args()

        if self.options.debug:
            logging.basicConfig(
                format='[%(levelname)s] (%(module)s) %(message)s')
            logger = logging.getLogger("nagios")
            logger.setLevel(logging.DEBUG)
            logger.debug("==== BEGIN DEBUG ====")
            logger.debug("name: %s", self.name)
            logger.debug("version: %s", self.version)
            logger.debug("description: %s", self.description)
            if self.__class__.__name__ == "NagiosAuto":
                logger.debug("==== END DEBUG ====")

    def define_options(self):
        self.parser.add_argument("--debug",
                                 action="store_true",
                                 dest="debug",
                                 help="Show debug information.")
