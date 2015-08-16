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

# from base import NagiosAuto
from application.application import Application
# from host.host import Host
# from service.service import Service
# from deploy.deploy import Deploy
# from web.web import Web


class NRobot(Application):
    def define_options(self):
        super(NRobot, self).define_options()
        self.required_args.add_argument("--cg",
                                        action="store_true",
                                        dest="create_hostgroup",
                                        required=False,
                                        help="Specify to create new \
                                        application.")
        self.required_args.add_argument("--dg",
                                        action="store_true",
                                        dest="delete_hostgroup",
                                        required=False,
                                        help="Specify to delete application.")
        self.required_args.add_argument("--ct",
                                        action="store_true",
                                        dest="create_template",
                                        required=False,
                                        help="Specify to create new template.")
        self.required_args.add_argument("-dt",
                                        action="store_true",
                                        dest="delete_template",
                                        required=False,
                                        help="Specify to delete template.")
        self.required_args.add_argument("-ch",
                                        action="store_true",
                                        dest="create_host",
                                        required=False,
                                        help="Specify to create host.")
        self.required_args.add_argument("-dh",
                                        action="store_true",
                                        dest="delete_host",
                                        required=False,
                                        help="Specify to delete host.")
        self.required_args.add_argument("-cs",
                                        action="store_true",
                                        dest="create_service",
                                        required=False,
                                        help="Specify to create service.")
        self.required_args.add_argument("-ds",
                                        action="store_true",
                                        dest="delete_service",
                                        required=False,
                                        help="Specify to delete template.")


def main():
    robot = NRobot()
    robot.logger.debug("in main")

    if robot.args.create_hostgroup:
        robot.create_hostgroup()
    elif robot.args.delete_hostgroup:
        robot.delete_hostgroup()



if __name__ == "__main__":
    main()
