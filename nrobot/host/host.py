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

        if self.args.file:
            self.file = self.args.file
        else:
            self.file = self.host_conf + "host.txt"
        self.fr = open(self.file, "r")
        self.lines = self.fr.readlines()

        self.area_list = ["as", "us", "eu"]

        if self.__class__.__name__ == "Host":
            self.logger.debug("==== END DEBUG ====")

    def define_options(self):
        """Define some options used for create host."""
        super(Host, self).define_options()
        self.parser.add_argument("-t", "--type",
                                 action="append",
                                 dest="type",
                                 required=False,
                                 help="The host type, eg: ['ad', 'mii', \
                                 'ijcore', 'mii_win-primary', 'mii_win-bck']. \
                                 Read template from type.cfg and \
                                 read hostname and ip address from type.txt. \
                                 Use type@mode for normal host. \
                                 mode=0 use dns as address. \
                                 mode=1 use ip as address.")
        self.parser.add_argument("-v", "--vcenter",
                                 dest="vcenter",
                                 required=False,
                                 help="Vcenter for mii and ijcore vmware.")
        self.parser.add_argument("-f", "--file",
                                 dest="file",
                                 required=False,
                                 help="Write the hostname your want to delete \
                                 here.")

    def get_area(self, hostname):
        """Get the area us/eu/as according to hostname."""
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

    def get_vcenter(self, vcenter):
        """Get the vcenter for vmware."""
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

    def get_mii_site(self, hostname):
        """Get the for _MII_SITEDATABASE in mii primary or backup server."""
        mii_site = hostname[2:5].upper()
        self.logger.debug("mii_site: {}".format(mii_site))
        return mii_site

    def get_type(self, type):
        if type in ["ad", "mii_win-primary", "mii_win-bck"]:
            type = type
            mode = 1
        elif type in ["mii", "ijcore"]:
            type = type
            mode = 0
        else:
            type = type.split("@")[0]
            mode = type.split("@")[1]
            if not mode:
                self.error("Please specify address mode for normal host.")
        self.logger.debug("type: {}".format(type))
        self.logger.debug("mode: {}".format(mode))
        return type, mode

    def write_one_host(self, hostfile, lines, vcenter,
                       area, mii_site, hostname, address):
        """Write to one host file."""
        fw = open(hostfile, "w")
        for l in lines:
            self.logger.debug("l: {}".format(l))
            if "ohtpl_area_%s" in l:
                fw.write(l % area)
            elif "ohtpl_sys_vmware_%s_%s" in l:
                l_vcenter = l.replace("ohtpl_sys_vmware_%s_%s", str(vcenter))
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

    def create_host(self):
        """Get type from -t and read hostname and address and write to the \
            hosts in nagios."""
        try:
            vcenter = ""
            area = ""
            mii_site = ""
            for loop in range(0, len(self.args.type)):
                type = self.args.type[loop]
                (type, mode) = self.get_type(type)

                # Get the template file.
                template = self.host_conf + type + ".cfg"
                self.logger.debug("template: {}".format(template))
                ftr = open(template, "r")
                lines = ftr.readlines()

                # Get the hostname and address file.
                host = self.host_conf + type + ".txt"
                self.logger.debug("host: {}".format(host))
                fhr = open(host, "r")
                h_lines = fhr.readlines()

                for line in h_lines:
                    hostname = line.split()[0].split(".")[0].strip().upper()
                    self.logger.debug("hostname: {}".format(hostname))
                    address = line.split()[int(mode)].strip().lower()
                    self.logger.debug("address: {}".format(address))
                    hostfile = self.g_dir + hostname + ".cfg"
                    self.logger.debug("hostfile: {}".format(hostfile))

                    if type in ["ad"]:
                        area = self.get_area(hostname)
                    elif type in ["mii_win-primary", "mii_win-bck"]:
                        area = self.get_area(hostname)
                        mii_site = self.get_mii_site(hostname)
                    elif type in ["mii", "ijcore"]:
                        if self.args.vcenter:
                            vcenter = self.get_vcenter(self.args.vcenter)
                        else:
                            self.error("Please use -v to specify vcenter.")

                    # Write to the host in nagios.
                    if os.path.isfile(hostfile):
                        self.already_exist("%s" % hostfile)
                        if self.args.force:
                            self.write_one_host(hostfile, lines, vcenter, area,
                                                mii_site, hostname, address)
                    else:
                        self.write_one_host(hostfile, lines, vcenter, area,
                                            mii_site, hostname, address)
        except Exception as e:
            self.error("create_host: %s" % e)

    def delete_host(self):
        for line in self.lines:
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
