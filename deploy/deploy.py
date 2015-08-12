#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright C 2015 Faurecia (China) Holding Co.,Ltd.                 #
# All rights reserved                                                #
# Name: deploy.py
# Author: Canux canuxcheng@163.com                                   #
# Version: V1.0                                                      #
# Time: Mon 10 Aug 2015 10:18:25 PM EDT
######################################################################
# Description:
######################################################################

import os
import sys
import commands
import argparse


parser = argparse.ArgumentParser(description="This script use git to deploy \
                                 nagios configuration to nagios server.")
parser.add_argument("-P", "--path",
                    default="/home/chengca/faurecia-nagios-configuration",
                    dest="path",
                    required=False,
                    help="Ths path of faurecia-nagios-configuration.")
parser.add_argument("-b", "--branch",
                    dest="branch",
                    required=False,
                    help="The branch you want to switch.")
parser.add_argument("-d", "--delete",
                    dest="delete",
                    required=False,
                    help="The branch you want to delete.")
args = parser.parse_args()

branch_list = ["master", "incubator", "develop"]
prefix = "request"
parent = "master"


def get_branch(pre_branch):
    if pre_branch in branch_list:
        branch = pre_branch
    else:
        branch = "%s/%s" % (prefix, pre_branch)
    return branch


def git_checkout(branch, parent):
    if args.branch:

    try:
        cmd = "git checkout %s" % branch
        (status, output) = commands.getstatusoutput(cmd)
        if status:
            try:
                cmd = "git checkout -b %s %s" % (branch, parent)
                (exitstatus, newoutput) = commands.getstatusoutput(cmd)
                if exitstatus:
                    print "# %s failed." % cmd
                    print ">>> %s <<<" % newoutput
                # If new branch created. Is this info necessary?
                else:
                    print "# Now, you are in new branch %s." % branch
                    print ">>> %s <<<" % newoutput
            except Exception:
                print "Err: git_checkout to new branch failed. \
                    Please investigate."
                sys.exit()
        # If checkout to new branch successed. Is this info necessary?
        else:
            print "# Now, you are in old branch %s." % branch
            print ">>> %s <<<" % output
    except Exception:
        print "Err: git_checkout to old branch failed. Please investigate."
        sys.exit()


def git_delete(branch, parent):
    try:
        cmd = "git checkout %s" % parent
        (status, output) = commands.getstatusoutput(cmd)
        if status:
            print "# git checkout %s failed." % parent
            print ">>> %s <<<" % output
        cmd = "git branch -D %s" % branch
        (status, output) = commands.getstatusoutput(cmd)
        if status:
            print "# git branch -D %s failed." % branch
            print ">>> %s <<<" % output
    except Exception:
        print "Err: git_delete failed. Please investigate."


def main():
    os.chdir(args.path)
    if args.branch:
        branch = get_branch(args.branch)
        git_checkout(branch, parent)
    elif args.delete:
        branch = get_branch(args.delete)
        git_delete(branch, parent)

if __name__ == "__main__":
    main()
