#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright (C) 2015 Faurecia (China) Holding Co.,Ltd.               #
# All rights reserved                                                #
# Name: host.py
# Author: Canux canuxcheng@gmail.com                                 #
# Version: V1.0                                                      #
# Time: Thu 20 Aug 2015 02:27:23 AM EDT
######################################################################
# Description:
######################################################################

from base import NagiosAuto
import os


class Host(NagiosAuto):
    """This class have three options to create create host file in nagios.
    You can specify the template you need.
    If you create a lots of host file at one time, this is more effeciency.
    """
    def __init__(self, *args, **kwargs):
        """Define some variables"""
        super(Host, self).__init__(*args, **kwargs)

        self.g_dir = self.args.path + "/hosts/"
        self.host_conf = self.conf + "/host/"
        self.area_conf = self.conf + "/area/"

        self.area_list = ["as", "us", "eu"]

        if self.__class__.__name__ == "Host":
            self.logger.debug("==== END DEBUG ====")

    def define_options(self):
        """Define some options used for create host."""
        super(Host, self).define_options()
        self.parser.add_argument("-t", "--types",
                                 action="append",
                                 dest="types",
                                 default=1,
                                 required=False,
                                 help="The host types, eg: ['ad', 'mii', \
                                 'ijcore', 'mii_win-primary', 'mii_win-bck']. \
                                 Read template from types.cfg and \
                                 read hostname and ip address from types.txt. \
                                 Use [types@mode] for normal host. \
                                 mode=0 use dns as address. \
                                 mode=1 use ip as address.")
        self.parser.add_argument("-v", "--vcenter",
                                 dest="vcenter",
                                 required=False,
                                 help="Vcenter for mii and ijcore vmware.")
        self.parser.add_argument("-m", "--miisite",
                                 dest="miisite",
                                 required=False,
                                 help="_MII_SITEDATABASE for mii_win-primary \
                                 and mii_win-bck")

    def get_area(self, hostname):
        """Get the area us/eu/as according to hostname."""
        try:
            locate = hostname[0:2].upper()
            self.logger.debug("locate: {}".format(locate))
            for area in self.area_list:
                area_file = self.area_conf + area + ".txt"
                self.logger.debug("area_file: {}".format(area_file))
                f = open(area_file, "r")
                lines = f.readlines()
                for line in lines:
                    if locate in line:
                        self.logger.debug("area: {}".format(area))
                        return area
            self.not_exist(locate)
        except Exception as e:
            self.error("get_area: %s" % e)

    def get_vcenter(self, vcenter):
        """Get the vcenter for vmware."""
        try:
            vcenterfile = self.area_conf + "vmware.txt"
            self.logger.debug("vcenterfile: {}".format(vcenterfile))
            fr = open(vcenterfile, "r")
            lines = fr.readlines()
            for line in lines:
                if vcenter in line:
                    vcenter = "".join(line.split())
                    self.logger.debug("vcenter: {}".format(vcenter))
                    return vcenter
            self.not_exist("%s" % vcenter)
        except Exception as e:
            self.error("get_vcenter: %s" % e)

    def get_types(self, types):
        try:
            if types in ["ad", "mii_win-primary", "mii_win-bck"]:
                types = types
                mode = 1
            elif types in ["mii", "ijcore"]:
                types = types
                mode = 0
            else:
                old_type = types
                types = old_type.split("@")[0]
                mode = old_type.split("@")[1]
                if not mode:
                    self.error("Please specify address mode for normal host.")
            self.logger.debug("types: {}".format(types))
            self.logger.debug("mode: {}".format(mode))
            return types, mode
        except Exception as e:
            self.error("get_types: %s" % e)

    def write_one_host(self, hostfile, lines, vcenter,
                       area, mii_site, hostname, address, env):
        """Write to one host file."""
        try:
            fw = open(hostfile, "w")
            for l in lines:
                self.logger.debug("l: {}".format(l))
                if "ohtpl_area_%s" in l:
                    fw.write(l % area)
                elif "ohtpl_env_%s" in l:
                    if env:
                        fw.write(l % env)
                elif "ohtpl_sys_vmware_%s_%s" in l:
                    l_vcenter = l.replace("ohtpl_sys_vmware_%s_%s",
                                          str(vcenter))
                    fw.write(l_vcenter)
                elif "host_name" in l:
                    fw.write(l % hostname)
                elif "address" in l:
                    fw.write(l % address)
                elif "_MII_SITEDATABASE" in l:
                    fw.write(l % mii_site)
                elif "%s" not in l:
                    fw.write(l)
                # If %s inside but not specify, can not handle it.
                else:
                    self.error("write_host: unknow argument %s inside.")
        except Exception as e:
            self.error("write_one_host: %s" % e)

    def create_host(self):
        """Get types from -t and read hostname and address and write to the \
            hosts in nagios."""
        try:
            vcenter = ""
            area = ""
            mii_site = ""
            env = ""
            for loop in range(0, len(self.args.types)):
                types = self.args.types[loop]
                self.logger.debug("types: {}".format(types))
                (types, mode) = self.get_types(types)

                # Get the template file.
                template = self.host_conf + types + ".cfg"
                self.logger.debug("template: {}".format(template))
                ftr = open(template, "r")
                lines = ftr.readlines()

                # Get the hostname and address file.
                host = self.host_conf + types + ".txt"
                self.logger.debug("host: {}".format(host))
                des_host = self.host_conf + types + ".tmp"
                self.logger.debug("des_host: {}".format(des_host))
                self.delete_blank_line(host, des_host)
                fhr = open(des_host, "r")
                h_lines = fhr.readlines()

                for line in h_lines:
                    hostname = line.split()[0].split(".")[0].strip().upper()
                    self.logger.debug("hostname: {}".format(hostname))
                    address = line.split()[int(mode)].strip().lower()
                    self.logger.debug("address: {}".format(address))
                    if len([i for i in line.split() if i]) == 3:
                        env = line.split()[2].strip().lower()
                        self.logger.debug("env: {}".format(env))
                    hostfile = self.g_dir + hostname + ".cfg"
                    self.logger.debug("hostfile: {}".format(hostfile))

                    area = self.get_area(hostname)
                    if types in ["mii_win-primary", "mii_win-bck"]:
                        if self.args.miisite:
                            mii_site = self.args.miisite.upper()
                        else:
                            self.error("Please use -m to specify \
                                       _MII_SITEDATABASE")
                    elif types in ["mii", "ijcore"]:
                        if self.args.vcenter:
                            vcenter = self.get_vcenter(self.args.vcenter)
                        else:
                            self.error("Please use -v to specify vcenter.")

                    # Write to the host in nagios.
                    if os.path.isfile(hostfile):
                        self.already_exist("%s" % hostfile)
                        if self.args.force:
                            self.write_one_host(hostfile, lines, vcenter,
                                                area, mii_site, hostname,
                                                address, env)
                    else:
                        self.write_one_host(hostfile, lines, vcenter, area,
                                            mii_site, hostname, address, env)
        except Exception as e:
            self.error("create_host: %s" % e)

    def delete_host(self):
        files = self.host_conf + "host.txt"
        self.logger.debug("files: {}".format(files))
        des_files = self.host_conf + "host.tmp"
        self.logger.debug("des_files: {}".format(des_files))
        self.delete_blank_line(files, des_files)
        self.fr = open(des_files, "r")
        self.lines = self.fr.readlines()
        for line in self.lines:
            self.logger.debug("line: {}".format(line))
            hostname = line.split()[0].split(".")[0].strip().upper()
            hostfile = self.g_dir + hostname + ".cfg"
            self.logger.debug("hostfile: {}".format(hostfile))
            if not os.path.isfile(hostfile):
                self.not_exist("%s" % hostfile)
            else:
                try:
                    os.remove(hostfile)
                except Exception as e:
                    self.error("remove_host: %s" % e)
