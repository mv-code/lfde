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

class Finish(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.title = "Finish"
        self.source = "finish.xml"

    def load_page(self):

        self.txt_log_path = self.frontend.builder.get_object("txt_log_path")
        self.txt_log_path.set_text(self.frontend.backend.main.logger.path)


    def page_enter(self):
        self.frontend.gui_set_sensitive("btn_forward", False)
        self.frontend.gui_set_sensitive("btn_back", False)

    def page_leave(self):
        pass

    def hook_forward(self):
        # reboot the system
        subprocess.call(["shutdown", "-r", "now"])

        # prevent the main module from calling the next page
        return False

