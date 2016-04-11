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

from Drive import Drive

class DriveScan:
    def __init__(self):
        pass

    def get_drive_list(self):
        drives = []

        part_fh = open("/proc/partitions", "r")

        i = 0
        for line in part_fh:
            #skip the first 2 lines
            if i < 2:
                i += 1
                continue;

            line = line.rstrip().lstrip()
            fields = line.split()
            name = fields[3]

            # we're only interested in sd* devices
            if re.match(r"sd[a-z]+$", name):
                size = self.get_size(name)
                drives.append(Drive(name, size))

        part_fh.close()

        return drives

    def get_size(self, device):
        block_fh = open("/sys/block/" + device + "/size")
        size = int(block_fh.read().rstrip())
        return size


if __name__ == "__main__":
    ds = DriveScan()
    ds.get_drive_list()
