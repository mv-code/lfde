#!/usr/bin/python
#
# LFDE - Linux Full Disk Encryption
# A program to set up true full disk encryption with USB key authentication
# Copyright (C) 2010 Mark Knowles <mark@lfde.org>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2, as published by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 

import os
import sys
import getopt
import shutil
import socket
import tempfile

from lfde.Choices import Choices
from lfde.CommitThread import CommitThread

from lfde.commit.ConfigCommit import ConfigCommit
from lfde.commit.FormatCommit import FormatCommit
from lfde.commit.PartitionCommit import PartitionCommit
from lfde.commit.GpgCommit import GpgCommit
from lfde.commit.MountCommit import MountCommit
from lfde.commit.BootSchemeCommit import BootSchemeCommit
from lfde.commit.LuksCommit import LuksCommit
from lfde.commit.InitramfsCommit import InitramfsCommit
from lfde.commit.GrubCommit import GrubCommit
from lfde.commit.BootSchemeCommit import BootSchemeCommit
from lfde.commit.InhibitAutoMountCommit import InhibitAutoMountCommit
from lfde.commit.RestoreAutoMountCommit import RestoreAutoMountCommit

 
class Backend:
    def __init__(self, main):
        self.commit_tasks = [ConfigCommit, InhibitAutoMountCommit, PartitionCommit, FormatCommit,
                MountCommit, GpgCommit, LuksCommit, GrubCommit, InitramfsCommit, \
                BootSchemeCommit, RestoreAutoMountCommit]

        self.main = main

        self.total_weight = 0
        for commit_task in self.commit_tasks:
            self.total_weight +=  commit_task.weight


    def commit(self, choices, commit_page):
        self.commit_page = commit_page

        tasks = []

        for task in self.commit_tasks:
            new_task = task(commit_page, choices, self.task_progress)
            tasks.append(new_task)

        self.current_task_id = 0
        self.task_start_progress = 0.0

        print "Starting commit thread"
        commit_thread = CommitThread(tasks, self.task_complete, self.commit_page.all_complete)
        commit_thread.start()


    def task_progress(self, percent_complete):
        """Called by the threads to update a tasks progress"""
        self.progress = self.task_start_progress

        # calculate what percent of the progress bar this task
        # takes up
        task_weight = self.commit_tasks[self.current_task_id].weight
        task_slice = float(task_weight) / float(self.total_weight)
        self.progress = self.progress + (percent_complete * task_slice)

        print "Setting task progress"
        self.commit_page.set_progress(self.progress)


    def task_complete(self, id):
        """Called by the task thread when a task is complete"""
        self.task_start_progress = self.progress
        self.current_task_id = id + 1

        print "Task complete"
        self.commit_page.task_complete(id)
