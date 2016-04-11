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
import re
import sys
import subprocess
from threading import Thread

from CommitTask import CommitTask

class PartitionCommit(CommitTask):
    name = "Partition USB Key"
    weight = 10

    def __init__(self, commit_page, choices, progress_callback):
        CommitTask.__init__(self, commit_page, choices, progress_callback)

    def run(self):
        print "Creating partition on: " + self.choices.usb_key_device
        self.partition(self.choices.usb_key_device)
        self.progress_callback(1.0)


    def partition(self, device):
        # -D gives a post-MBR gap that grub needs
        sfdisk_proc = subprocess.Popen(["sfdisk", "-q", "-D", device], stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        sfdisk_proc.stdin.write(";;;*\n")
        sfdisk_proc.stdin.close()
        if sfdisk_proc.wait() != 0:
            print "sfdisk error"
