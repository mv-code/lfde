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

class Format(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.title = "Choose USB Key Filesystem"
        self.source = "format.xml"

    def load_page(self):

        self.lb_filesystems = self.frontend.builder.get_object("lb_filesystems")
        self.lb_filesystems_model = self.lb_filesystems.get_data_model()

        self.lb_filesystems_model.append(["ext4"])
        self.lb_filesystems_model.append(["ext3"])

    def page_leave(self):
        self.frontend.choices.fs_type = self.lb_filesystems_model.get_selected()[0]


