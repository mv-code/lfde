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

import gtk
from lfde.util.DeviceUnmounter import DeviceUnmounter
from lfde.util.UnmountableException import UnmountableException

class Unmount(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.source = "unmount.glade"
        self.title = "Unmount Partitions"
        self.root_object_name = "root_unmount"

        self.device_unmounter = DeviceUnmounter(self.frontend.choices.usb_key_device)

    def load_page(self):
        self.frontend.builder.connect_signals({"on_btn_unmount_clicked" : self.on_btn_unmount_clicked})
        self.trv_mounted = self.frontend.builder.get_object("trv_mounted")

        self.trv_mounted_model = gtk.ListStore(str, str)
        self.trv_mounted.set_model(self.trv_mounted_model)

        column_0 = gtk.TreeViewColumn('Device')

        cell_renderer_0 = gtk.CellRendererText()
        column_0.pack_start(cell_renderer_0, True)
        column_0.add_attribute(cell_renderer_0, 'text', 0)
        self.trv_mounted.append_column(column_0)

        column_1 = gtk.TreeViewColumn('Mountpoint')

        cell_renderer_1 = gtk.CellRendererText()
        column_1.pack_start(cell_renderer_1, True)
        column_1.add_attribute(cell_renderer_1, 'text', 1)
        self.trv_mounted.append_column(column_1)

        self.trv_mounted_tree_selection = self.trv_mounted.get_selection()


    def page_enter(self):
        # two columns: Device | Mount Point

        self.device_unmounter = DeviceUnmounter(self.frontend.choices.usb_key_device)

        # user cannot go forward until all mounted partitions are
        # unmounted
        # check to see if there are actually any mounted partitions.
        # if not, skip the whole page
        self.frontend.gui_set_sensitive("btn_forward", False)
        mounted = self.device_unmounter.get_mounted()
        if len(mounted) == 0:
            self.frontend.skip()
        else:
            # populate the gui with the devices
            self.refresh_list()

    def refresh_list(self):
        self.trv_mounted_model.clear()
        mounted = self.device_unmounter.get_mounted()
        for mounted_device in mounted:
            self.trv_mounted_model.append([mounted_device.device, mounted_device.mountpoint])

        if len(mounted) == 0:
            self.frontend.gui_set_sensitive("btn_forward", True)
        else:
            self.frontend.gui_set_sensitive("btn_forward", False)

    def on_btn_unmount_clicked(self, data):
        try:
            self.device_unmounter.unmount_all()
        except UnmountableException, ex:
            # tell the user the bad news
            self.frontend.message_box(ex.description)

        self.refresh_list()
