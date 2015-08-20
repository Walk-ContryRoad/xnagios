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

import commands
from base import NagiosAuto


class Deploy(NagiosAuto):
    def __init__(self, *args, **kwargs):
        super(Deploy, self).__init__(*args, **kwargs)
        self.parent = "master"
        self.branch_list = ["master", "incubator", "develop"]
        self.prefix = "request"
        if self.args.branch in self.branch_list:
            self.branch = self.args.branch
        else:
            self.branch = "%s/%s" % (self.prefix, self.args.branch)

    def define_options(self):
        super(Deploy, self).define_options()
        self.parser.add_argument("-b", "--branch",
                                 dest="branch",
                                 required=False,
                                 help="The branch you want to switch.")
        self.parser.add_argument("-c", "--comment",
                                 default="[MC]Modify the configuration.",
                                 dest="comment",
                                 required=False,
                                 help="Commit comment like [APP]comments.")

    def status_branch(self, branch):
        try:
            cmd = "git status"
            (status, output) = commands.getstatusoutput(cmd)
            self.logger.debug(cmd, output)
            if "Untracked files" in output or \
                    "Changes to be committed" in output:
                choice = input("%s\nCommit this files? " % output)
                if choice == 0:
                    comment = input("Input commit comment: ")
                    self.commit_branch(comment)
        except Exception as e:
            self.error("Error status_branch: %s" % e)

    def create_branch(self, branch):
        try:
            cmd = "git checkout %s" % branch
            (status, output) = commands.getstatusoutput(cmd)
            self.logger.debug("{0}: {1}".format(cmd, output))
            # If this branch is not exist.
            if status:
                cmd1 = "git checkout -b %s %s" % (branch, self.parent)
                (status1, output1) = commands.getstatusoutput(cmd1)
                self.logger.debug("{0}: {1}".format(cmd1, output1))
                if not status1:
                    return output1
            # If this branch exist.
            else:
                self.already_exist(branch)
                return output
        except Exception as e:
            self.error("Error create_branch: %s" % e)

    def delete_branch(self, branch):
        try:
            # Checkout to master to delete other branch.
            self.create_branch(self.parent)
            cmd1 = "git branch -D %s" % branch
            (status1, output1) = commands.getstatusoutput(cmd1)
            self.logger.debug("{0}: {1}".format(cmd1, output1))
            if status1:
                self.not_exist(branch)
        except Exception as e:
            self.error("Error delete_branch: %s" % e)

    def commit_branch(self, comment):
        try:
            cmd = "git add -A ."
            (status, output) = commands.getstatusoutput(cmd)
            self.logger.debug("{0}: {1}".format(cmd, output))
            if not status:
                cmd1 = "git commit -a -m %s" % comment
                (status1, output1) = commands.getstatusoutput(cmd1)
                self.logger.debug("{0}: {1}".format(cmd1, output1))
        except Exception as e:
            self.error("Error commit_branch: %s" % e)

    def asyn_branch(self, branch, output):
        if branch in self.branch_list:
            try:
                if "have diverged" in output:
                    self.commit_branch(self.args.comment)
                    cmd = "git reset --hard origin/%s" % branch
                    (status, output) = commands.getestatusoutput(cmd)
                    self.logger.debug("{0}: {1}".format(cmd, output))
                elif "fast-forwarded" in output:
                    cmd1 = "git fetch -p"
                    (status1, output1) = commands.getstatusoutput(cmd1)
                    self.logger.debug("{0}: {1}".format(cmd1, output1))
                    cmd2 = "git pull"
                    (status2, output2) = commands.getstatusoutput(cmd2)
                    self.logger.debug("{0}: {1}".format(cmd2, output2))
            except Exception as e:
                self.error("Error asyn_branch %s" % e)

    def merge_branch(self, branch):
            try:
                cmd = "git merge --no-ff %s" % branch
                (status, output) = commands.getstatusoutput(cmd)
                self.logger.debug("{0}: {1}".format(cmd, output))
                if "Automatic merge failed" in output:
                    cmd1 = "git mergetool --tool=meld"
                    (status1, output1) = commands.getstatusoutput(cmd1)
                    self.logger.debug("{0}: {1}".format(cmd1, output1))
                    # Delete the *.cfg.orig file.
                    if not status1:
                        cmd2 = "find . -name '*.orig' | xargs rm -f"
                        (status2, output2) = commands.getstatusoutput(cmd2)
                        self.logger.debug("{0}: {1}".format(cmd2, output2))
                        # Commit.
                        if not status2:
                            cmd3 = "git commit"
                            (status3, output3) = commands.getstatusoutput(cmd3)
                            self.logger.debug("{0}: {1}".format(cmd3, output3))
                # Push at last.
                cmd = "git push"
                (status, output) = commands.getstatusoutput(cmd)
                self.logger.debug("{0}: {1}".format(cmd, output))
            except Exception as e:
                self.error("Error merge_branch: %s" % e)

    def deploy_branch(self):
        for branch in ["develop", "incubator"]:
            choice = self.input("Are you sure deploy on %s? " % branch)
            if choice == 0:
                output = self.create_branch(branch)
                self.asyn_branch(branch, output)
                self.merge_branch(self.branch)
                try:
                    cmd = "fab  gearman.deploy"
                    (status, output) = commands.getstatusoutput(cmd)
                    self.logger.debug(cmd, output)
                except Exception as e:
                    self.error("Error deploy_branch: %s" % e)
