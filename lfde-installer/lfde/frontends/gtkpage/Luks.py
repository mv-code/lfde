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
import gtk

from ..Page import Page

class Luks(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.title = "LUKS Passphrase"
        self.source = "luks.glade"
        self.root_object_name = "root_luks"

    def load_page(self):

        self.frontend.builder.connect_signals({"on_btn_check_clicked" : self.on_btn_check_clicked})


        self.txt_luks_passphrase = self.frontend.builder.get_object("txt_luks_passphrase")
        self.lbl_ok = self.frontend.builder.get_object("lbl_ok")
        self.lbl_not_ok = self.frontend.builder.get_object("lbl_not_ok")
        self.btn_check = self.frontend.builder.get_object("btn_check")


    def page_enter(self):
        #TODO: change this to False when we get our check method working
        self.frontend.gui_set_sensitive("btn_forward", True)

    def page_leave(self):
        self.frontend.choices.luks_old_key = self.txt_luks_passphrase.get_text()

    def on_btn_check_clicked(self, data):
        pass
