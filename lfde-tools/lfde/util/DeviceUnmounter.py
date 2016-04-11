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

import string
import subprocess

from MountedDevice import MountedDevice
from UnmountableException import UnmountableException

class DeviceUnmounter:
    def __init__(self, target_device):
        self.target_device = target_device

    def refresh(self):
        self.mounted = self.find_mounted()

    def get_mounted(self):
        self.refresh()
        
        return self.mounted

    def unmount_all(self):
        for mounted_device in self.mounted:
            retcode = subprocess.call(["umount", mounted_device.device])

        self.refresh()

        if len(self.mounted) > 0:
            raise UnmountableException(self.mounted)

    def find_mounted(self):
        """Note this only support sd* devices
           or checking the actual device itself"""
        mounts_fh = open("/proc/mounts")

        mounted = []
        while True:
            line = mounts_fh.readline()
            if not line:
                break

            fields = line.split()
            device = fields[0]
            mountpoint = fields[1]

            if device == self.target_device or device.startswith(self.target_device):
                mounted.append(MountedDevice(device, mountpoint))

        return mounted
