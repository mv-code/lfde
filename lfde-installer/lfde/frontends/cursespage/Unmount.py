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

from lfde.util.DeviceUnmounter import DeviceUnmounter
from lfde.util.UnmountableException import UnmountableException

class Unmount(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.source = "unmount.xml"
        self.title = "Unmount Partitions"
        self.root_object_name = "root_unmount"

    def load_page(self):
        self.frontend.builder.connect_signals({"on_btn_unmount_clicked" : self.on_btn_unmount_clicked})

        self.lb_unmount = self.frontend.builder.get_object("lb_unmount")
        self.lb_unmount_model = self.lb_unmount.get_data_model()

    def page_enter(self):
        # two columns: Device | Mount Point

        self.device_unmounter = DeviceUnmounter(self.frontend.choices.usb_key_device)

        # user cannot go forward until all mounted partitions are
        # unmounted
        # check to see if there are actually any mounted partitions.
        # if not, skip the whole page
        self.frontend.gui_set_sensitive("btn_forward", False)

        self.refresh_list()
        if len(self.mounted) == 0:
            self.frontend.skip()
        else:
            # populate the gui with the devices
            self.refresh_list()
            pass

    def refresh_list(self):
        self.mounted = self.device_unmounter.get_mounted()
        self.lb_unmount_model.clear()
        for mounted_device in self.mounted:
            self.lb_unmount_model.append([mounted_device.device, mounted_device.mountpoint])

        if len(self.mounted) == 0:
            self.frontend.gui_set_sensitive("btn_forward", True)
        else:
            self.frontend.gui_set_sensitive("btn_forward", False)

    def on_btn_unmount_clicked(self):
        try:
            print "Attempting unmount"
            self.device_unmounter.unmount_all()
        except UnmountableException, ex:
            # tell the user the bad news
            print ex.description
            frontend.message_box(ex.description)

        self.refresh_list()
