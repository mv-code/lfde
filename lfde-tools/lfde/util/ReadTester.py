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
from threading import Thread

import datetime

class ReadTester(Thread):
    def __init__(self, usb_key_device):
        Thread.__init__(self)

        self.usb_key_device = usb_key_device
        self.running = False
        self.stopping = False


    def run(self):
        self.running = True
        usb_key_fh = open(self.usb_key_device)
        while self.stopping == False:
            data = usb_key_fh.read(1024)

            if len(data) <= 0:
                # restart
                usb_key_fh.seek(0)

        usb_key_fh.close()
        self.running = False
        self.stopping = False

    def stop(self):
        self.stopping = True

