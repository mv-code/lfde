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

import gtk
import gobject

# TODO:
# 1. Keep rescanning for device insertion (maybe use udev?)

class UsbKey(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.title = "Create/choose USB key"
        self.source = "usbkey.glade"
        self.root_object_name = "root_usbkey"

    def load_page(self):
        self.trv_drives = self.frontend.builder.get_object("trv_drives")
        self.frontend.builder.connect_signals({"on_trv_drives_cursor_changed" : self.on_trv_drives_cursor_changed})


        self.trv_drives_model = gtk.ListStore(str, str)
        self.trv_drives.set_model(self.trv_drives_model)

        column_0 = gtk.TreeViewColumn('Device')

        cell_renderer_0 = gtk.CellRendererText()
        column_0.pack_start(cell_renderer_0, True)
        column_0.add_attribute(cell_renderer_0, 'text', 0)
        self.trv_drives.append_column(column_0)

        column_1 = gtk.TreeViewColumn('Size (GB)')

        cell_renderer_1 = gtk.CellRendererText()
        column_1.pack_start(cell_renderer_1, True)
        column_1.add_attribute(cell_renderer_1, 'text', 1)
        self.trv_drives.append_column(column_1)

        self.trv_drives_tree_selection = self.trv_drives.get_selection()

    def page_enter(self):
        self.frontend.gui_set_sensitive("btn_forward", False)

        drive_scan = DriveScan()

        self.trv_drives_model.clear()
        for drive in drive_scan.get_drive_list():
            self.trv_drives_model.append([drive.get_device(), str(drive.get_gb_size())])


    def hook_forward(self):

        (model, iter) = self.trv_drives_tree_selection.get_selected()
        self.frontend.choices.usb_key_device = model.get_value(iter, 0)
        self.frontend.choices.usb_key_partition = self.frontend.choices.usb_key_device + "1"

        return True

    def on_trv_drives_cursor_changed(self, data):
        self.frontend.gui_set_sensitive("btn_forward", True)

