#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright (C) 2015 Faurecia (China) Holding Co.,Ltd.               #
# All rights reserved                                                #
# Name: service.py
# Author: Canux canuxcheng@gmail.com                                 #
# Version: V1.0                                                      #
# Time: Sun 08 Nov 2015 09:24:30 PM EST
######################################################################
# Description:
######################################################################

from base import NagiosAuto


class Service(NagiosAuto):
    """This class used to add services for servers.
    You can specify a file include your servers.
    And another file include your services.
    """
    def __init__(self, *args, **kwargs):
        """Define some variables"""
        super(Service, self).__init__(*args, **kwargs)

        self.service_conf = self.conf + "/service"

        if self.__class__.__name__ == "Service":
            self.logger.debug("==== END DEBUG ====")

    def define_options(self):
        """Define some options for create service."""
        super(Service, self).define_options()
        self.parser.add_argument("-t", "--type",
                                 action="append",
                                 dest="types",
                                 required=False,
                                 help="The service and host filename.\
                                 eg: -t 1234, then the program will remove\
                                 all services in 1234.cfg from all hosts in\
                                 1234.txt.")
