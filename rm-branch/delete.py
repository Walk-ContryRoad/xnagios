#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: delete.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Wed 15 Jul 2015 10:26:38 PM EDT
######################################################################
# Description:
######################################################################

import os
import sys
import requests
import commands
import argparse
import tempfile
from bs4 import BeautifulSoup


def define_arguments():
    parser = argparse.ArgumentParser(description="This script used for remove \
                                     branch from center repository.")
    parser.add_argument("-U", "--user",
                        dest="user",
                        required=False,
                        help="The user.Default is $USER.")
    parser.add_argument("-u", "--url",
                        dest="url",
                        required=False,
                        default="http://monitoring-dc.app.corp/tracking/news/",
                        help="The url.Default is \
                        http://monitoring-dc.app.corp/tracking/news/")
    parser.add_argument("-y", "--year",
                        type=int,
                        dest="year",
                        required=False,
                        default=2015,
                        help="The year.Default is 2015.")
    parser.add_argument("-w", "--week",
                        type=int,
                        action="append",
                        dest="week",
                        required=False,
                        help="Which week you want to remove. \
                        Remove all branchs which merge to master that week. \
                        You can use -w XXX -w XXX ... to remove a lots of \
                        weeks  at the same time.")
    parser.add_argument("-b", "--branch",
                        action="append",
                        dest="branch",
                        required=False,
                        help="Which branch you want to remove. \
                        You can use -b xxx -b xxx ... to remove a lots of \
                        branchs  at the same time.")
    parser.add_argument("-p", "--path",
                        dest="path",
                        required=False,
                        help="The path of faurecia-nagios-configuration. \
                        Start from \ folder.")
    args = parser.parse_args()

    # Change to faurecia-nagios-configuration folder.
    home = os.environ["HOME"]
    path = "faurecia-nagios-configuration"
    if args.path:
        g_dir = args.path
    else:
        output = commands.getoutput("sudo find %s -name %s" % (home, path))
        # If more than one path, you must assign one.
        if len(output.split()) != 1:
            print """More than one %s.
            Use -p to specify the path is adviced.""" % path
            g_dir = output.split()[0]
        else:
            g_dir = output
    print "Use: %s" % g_dir
    os.chdir(g_dir)

    # Get the username.
    if args.user:
        user = args.user
    else:
        user = os.getenv("USER")
    if args.url:
        url = args.url
    return args, user, url


# Get the news.
def get_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    info = soup.get_text()
    temp = tempfile.TemporaryFile("w+r")
    temp.writelines(info)
    temp.seek(0)
    lines = temp.readlines()
    return lines


# Get the lastlines.
def get_lastlines(lines, start, end):
    for loop in range(0, len(lines)):
        line = lines[loop]
        if line.startswith(start):
            startline = loop
        if line.startswith(end):
            endline = loop
            break
    if startline in locals().keys() and endline in locals().keys():
        lastlines = lines[startline:endline]
    else:
        print ">>> This week isn't exist on this page.<<<"
        lastlines = ""
    return lastlines


# Delete the branch.
def delete_branch(lastlines, user):
    for loop in range(0, len(lastlines)):
        line = lastlines[loop]
        if line.startswith("#"):
            number = line.split()[0].split("#")[1]
            os.system("git push -u origin :u/%s/request/%d" %
                      (user, int(number)))


# Main fucntion
def main():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    args, user, url = define_arguments()

    # Delete the specify branchs.
    if args.branch:
        for loop in range(0, len(args.branch)):
            number = args.branch[loop]
            os.system("git push -u origin :u/%s/request/%d" %
                      (user, int(number)))

    # Delete the specify weeks
    elif args.week:
        for loop in range(0, len(args.week)):
            week = args.week[loop]
            lines = get_url(url)
            newlines = get_lastlines(lines,
                                     "Nagios Integration - W%d-%d" %
                                     (week, args.year),
                                     "Nagios Integration")
            # This week not exist in this page.
            if not newlines:
                continue
            lastlines = get_lastlines(newlines,
                                      "Requests merged in production (MASTER)",
                                      "Requests kept-back in pre-production "
                                      "(INCUBATOR):")
            delete_branch(lastlines, user)

    # Default to delete the lastweek.
    else:
        lines = get_url(url)
        lastlines = get_lastlines(lines,
                                  "Requests merged in production (MASTER)",
                                  "Requests kept-back in pre-production "
                                  "(INCUBATOR):")
        delete_branch(lastlines, user)

if __name__ == "__main__":
    main()
