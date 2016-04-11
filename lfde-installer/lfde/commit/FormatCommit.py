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

class FormatCommit(CommitTask):
    name = "Format USB Key"
    weight = 10

    def __init__(self, commit_page, choices, progress_callback):
        CommitTask.__init__(self, commit_page, choices, progress_callback)


    def run(self):
        print "Formatting: " + self.choices.usb_key_partition + " as " + \
                self.choices.fs_type
        self.format(self.choices.usb_key_partition, self.choices.fs_type)
        self.progress_callback(1.0)


    def format(self, device, type):
        cmd = ["mkfs", "-L", "usbkey", "-t", type, device]
        #print cmd
        mkfs_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=sys.stderr)

        state = 1
        while True:
            line = mkfs_proc.stdout.readline()
            if not line:
                break

            if state == 1 and line.startswith("Superblock backups stored on blocks"):
                #print "Got superblock line"
                state = 2
                continue

            elif state == 2:
                # read lines until we get a blank line
                if len(line) == 1:
                    #print "Got blank line"

                    # read char by char
                    buf = ""
                    while True:
                        char = mkfs_proc.stdout.read(1)
                        if not char:
                            break

                        if char == "\n":
                            #print "Got end of progress"
                            state = 3
                            break

                        if ord(char) == 8:
                            if len(buf) != 0:
                                # we have a buffer in the form of number/number
                                # get rid of junk
                                match = re.search("(\d+)/(\d+)", buf)
                                #print match.group(0)
                                done = float(match.group(1))
                                total = float(match.group(2))

                                # now report progress to the callback
                                percent_complete = done / total
                                self.progress_callback(percent_complete)

                                buf = ""
                        else:
                            buf += char


        mkfs_proc.stdout.close()

