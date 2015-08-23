#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: nrobot.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Fri 14 Aug 2015 01:51:44 AM EDT
######################################################################
# Description:
######################################################################

import os
import sys
from application.application import Application
from deploy.deploy import Deploy
# from host.host import Host
# from service.service import Service
# from web.web import Web


class NRobot(Application, Deploy):
    def define_options(self):
        super(NRobot, self).define_options()
        self.required_args.add_argument("--cb",
                                        action="store_true",
                                        dest="create_branch",
                                        required=False,
                                        help="Specify to create or \
                                        checkout branch.")
        self.required_args.add_argument("--db",
                                        action="store_true",
                                        dest="delete_branch",
                                        required=False,
                                        help="Specify to delete branch.")
        self.required_args.add_argument("--cg",
                                        action="store_true",
                                        dest="create_hostgroup",
                                        required=False,
                                        help="Specify to create application.")
        self.required_args.add_argument("--dg",
                                        action="store_true",
                                        dest="delete_hostgroup",
                                        required=False,
                                        help="Specify to delete application.")
        self.required_args.add_argument("--ct",
                                        action="store_true",
                                        dest="create_template",
                                        required=False,
                                        help="Specify to create template.")
        self.required_args.add_argument("--dt",
                                        action="store_true",
                                        dest="delete_template",
                                        required=False,
                                        help="Specify to delete template.")
        self.required_args.add_argument("--ch",
                                        action="store_true",
                                        dest="create_host",
                                        required=False,
                                        help="Specify to create host.")
        self.required_args.add_argument("--dh",
                                        action="store_true",
                                        dest="delete_host",
                                        required=False,
                                        help="Specify to delete host.")
        self.required_args.add_argument("--cs",
                                        action="store_true",
                                        dest="create_service",
                                        required=False,
                                        help="Specify to create service.")
        self.required_args.add_argument("--ds",
                                        action="store_true",
                                        dest="delete_service",
                                        required=False,
                                        help="Specify to delete service.")


def main():
    robot = NRobot("nagiosauto", "1.0", "Config nagios automatic")
    os.chdir(robot.args.path)

    # What to do.
    argv = sys.argv[0]
    getcwd = os.getcwd()
    robot.logger.debug("argv[0]: {}".format(argv))
    robot.logger.debug("os.getcwd: {}".format(getcwd))

    robot.logger.debug("==== END DEBUG ====")


if __name__ == "__main__":
    main()
