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
from ..Page import Page
from lfde.util.DriveScan import DriveScan

# TODO:
# 1. Keep rescanning for device insertion (maybe use udev?)

class UsbKey(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.title = "Create/choose USB key"
        self.source = "usbkey.xml"

    def load_page(self):
        self.lb_drives = self.frontend.builder.get_object("lb_drives")
        self.lb_drives_model = self.lb_drives.get_data_model()

    def page_enter(self):
        self.frontend.gui_set_sensitive("btn_forward", True)

        drive_scan = DriveScan()

        self.lb_drives.clear()

        for drive in drive_scan.get_drive_list():
            self.lb_drives_model.append([drive.get_device(), str(drive.get_gb_size())])

    def hook_forward(self):

        self.frontend.choices.usb_key_device = self.lb_drives_model.get_selected()[0]
        self.frontend.choices.usb_key_partition = self.frontend.choices.usb_key_device + "1"

        self.frontend.builder.root_widget.debugln(self.frontend.choices.usb_key_device)

        return True

