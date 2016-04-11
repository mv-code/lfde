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

class BootScheme(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.title = "Boot scheme"
        self.source = "boot_scheme.xml"

    def load_page(self):
        self.lb_boot_scheme = self.frontend.builder.get_object("lb_boot_scheme")
        self.lb_boot_scheme_model = self.lb_boot_scheme.get_data_model()
        self.lb_boot_scheme_model.append(["Boot from USB"])
        self.lb_boot_scheme_model.append(["Boot from Hard Disk"])

    def page_enter(self):
        pass

    def page_leave(self):
        if self.lb_boot_scheme.get_selected_index() == 0:
            self.frontend.choices.boot_scheme = "usb"
        else:
            self.frontend.choices.boot_scheme = "hdd"

