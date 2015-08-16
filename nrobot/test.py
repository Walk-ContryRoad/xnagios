#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: test.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Thu 13 Aug 2015 04:25:08 AM EDT
######################################################################
# Description:
######################################################################

from application.application import Application

robot = Application()
# robot.create_hostgroup()
robot.delete_hostgroup()
