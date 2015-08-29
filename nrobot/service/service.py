#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: service.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Thu 27 Aug 2015 05:41:05 AM EDT
######################################################################
# Description:
######################################################################

from base import NagiosAuto

class Service(NagiosAuto):
    """This class used to create service for hosts in nagios."""
    def __init__(self):
        super(Service, self).__init__(*args, **kwargs)


