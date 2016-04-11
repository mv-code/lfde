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

class KillAll:

    def killall(self, target_name):
        for process in os.listdir("/proc"):
            file_path = os.path.join("/proc", process, "cmdline")

            if not os.access(file_path, os.R_OK):
                continue

            cmdline_fh = open(file_path)
            contents = cmdline_fh.read()
            name = contents.split("\0")[0]

            if name == target_name:
                os.kill(int(process), 9)
                print "Killed"

if __name__ == "__main__":
    killall = KillAll()
    killall.killall("/usr/lib/gvfs/gvfs-gdu-volume-monitor")
