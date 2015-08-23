#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: host.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Thu 20 Aug 2015 02:27:23 AM EDT
######################################################################
# Description:
######################################################################

from base import NagiosAuto


class Host(NagiosAuto):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        if self.__class__.__name__ == "Host":
            self.logger.debug("==== END DEBUG ====")

    def define_options(self):
        super(Host, self).define_options()

        self.parser.add_argument("-m", "--mode",
                                 dest="mode",
                                 required=False,
                                 help="address style. 0 use dns, 1 use ip.")
        self.parser.add_argument("-f", "--files",
                                 action="append",
                                 dest="files",
                                 help="Read hostname ip and templates from \
                                 this file.Without the prefix. \
                                 eg: -f app1 -f app2. \
                                 Read configuration from app1.cfg. \
                                 Read hostname and ip from app1.txt.")

    def get_host(self):

    def get_area(self):

    def create_host(self):

