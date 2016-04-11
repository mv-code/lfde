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
import tempfile
import subprocess

from CommitTask import CommitTask

class MountCommit(CommitTask):
    name = "Mount USB Key"
    weight = 5

    def __init__(self, commit_page, choices, progress_callback):
        CommitTask.__init__(self, commit_page, choices, progress_callback)

    def run(self):
        self.choices.mountpoint = tempfile.mkdtemp(dir="/media")
        print "Mounting USB key at: " + self.choices.mountpoint

        self.mount(self.choices.usb_key_partition, self.choices.mountpoint)
        self.progress_callback(1.0)


    def mount(self, device, mountpoint):
        retcode = subprocess.call(["mount", device, mountpoint])

        if retcode != 0:
            raise Exception("Couldn't mount USB key")

