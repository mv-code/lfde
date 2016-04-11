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
import shutil
import os.path
import subprocess

from CommitTask import CommitTask

class GrubCommit(CommitTask):
    name = "Configure Grub"
    weight = 10

    def __init__(self, commit_page, choices, progress_callback):
        CommitTask.__init__(self, commit_page, choices, progress_callback)


    def run(self):
        if self.choices.boot_scheme == "usb":


            grub_proc = subprocess.Popen(["grub-install", "--recheck", "--no-floppy", "--root-directory" + "=" + self.choices.mountpoint, \
                    self.choices.usb_key_device], \
                    stdout=sys.stdout, stderr=sys.stderr)

            if grub_proc.wait() != 0:
                raise Exception("grub-install failed")

            # Temporarily disabled to test something
            #shutil.copy("/usr/share/lfde-installer/grub.cfg", os.path.join(self.choices.mountpoint, "boot", "grub"))


            self.progress_callback(1.0)


