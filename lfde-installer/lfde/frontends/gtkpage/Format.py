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
import gtk
import subprocess

from ..Page import Page

class Format(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.title = "Choose USB Key Filesystem"
        self.source = "format.glade"
        self.root_object_name = "root_format"

    def load_page(self):

        self.cmb_filesystems = self.frontend.builder.get_object("cmb_filesystems")
        self.prg_format = self.frontend.builder.get_object("prg_format")

        self.cmb_filesystems_model = gtk.ListStore(str)
        self.cmb_filesystems.set_model(self.cmb_filesystems_model)
        cell = gtk.CellRendererText()
        self.cmb_filesystems.pack_start(cell, True)
        self.cmb_filesystems.add_attribute(cell, 'text', 0)

        # add in the filesystems
        self.cmb_filesystems_model.append(["ext3"])
        self.cmb_filesystems_model.append(["ext4"])
        self.cmb_filesystems.set_active(1)


    def page_leave(self):
        active = self.cmb_filesystems.get_active()
        if active < 0:
            raise Exception("Couldn't get filesystem option")

        self.frontend.choices.fs_type = self.cmb_filesystems_model[active][0]


