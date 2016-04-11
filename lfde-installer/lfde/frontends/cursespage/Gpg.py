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
import os
import string
import datetime

from ..Page import Page

class Gpg(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.title = "GNU Privacy Guard (GPG) Configuration"
        self.source = "gpg.xml"

    def load_page(self):

        self.frontend.builder.connect_signals({"on_txt_password_changed" : self.validate, \
                "on_txt_password_confirm_changed" : self.validate, \
                "on_txt_key_expiry_changed" : self.validate, \
                "on_chk_disable_password_toggled" : self.on_chk_disable_password_toggled })

        self.lb_key_type = self.frontend.builder.get_object("lb_key_type")
        self.lb_key_type_model = self.lb_key_type.get_data_model()
        self.lb_key_type_model.append(["RSA/RSA"])
        self.lb_key_type_model.append(["DSA/Elgamal"])
        self.spn_key_length = self.frontend.builder.get_object("spn_key_length")
        self.txt_password = self.frontend.builder.get_object("txt_password")
        self.txt_password_confirm = self.frontend.builder.get_object("txt_password_confirm")
        self.txt_email = self.frontend.builder.get_object("txt_email")
        self.txt_name = self.frontend.builder.get_object("txt_name")
        self.txt_comment = self.frontend.builder.get_object("txt_comment")
        self.txt_key_expiry = self.frontend.builder.get_object("txt_key_expiry")
        self.chk_disable_password = self.frontend.builder.get_object("chk_disable_password")
        #self.chk_use_entropy_generator = self.frontend.builder.get_object("chk_use_entropy_generator")

        self.txt_email.set_text(self.frontend.choices.email)
        self.txt_name.set_text(self.frontend.choices.gpg_name)
        self.txt_key_expiry.set_text(datetime.datetime.strftime( \
                self.frontend.choices.gpg_key_expiry_date, "%Y%m%d"))

    def page_enter(self):
        self.frontend.gui_set_sensitive("btn_forward", False)
        self.validate()

    def page_leave(self):

        if self.lb_key_type.get_selected_index() == 0:
            self.frontend.choices.gpg_key_type = "RSA" 
            self.frontend.choices.gpg_sub_key_type = "RSA"
        else:
            self.frontend.choices.gpg_key_type = "DSA" 
            self.frontend.choices.gpg_sub_key_type = "ELG-E"

        self.frontend.choices.gpg_key_length = self.spn_key_length.get_value()
        self.frontend.choices.gpg_password = self.txt_password.get_text()

        self.frontend.choices.gpg_email = self.txt_email.get_text()
        self.frontend.choices.gpg_name = self.txt_name.get_text()
        self.frontend.choices.gpg_comment = self.txt_comment.get_text()
        # TODO: implement entropy generator
        self.frontend.choices.gpg_use_entropy_generator = True

        self.frontend.choices.disable_password = self.chk_disable_password.get_active()
        self.frontend.choices.gpg_key_expiry_date = datetime.datetime.strptime(string.strip(self.txt_key_expiry.get_text()), "%Y%m%d")

    def on_chk_disable_password_toggled(self):
        # disable/enable all the GPG fields
        if self.chk_disable_password.get_active() == True:
            self.set_gpg_widgets_sensitive(False)
        else:
            self.set_gpg_widgets_sensitive(True)

        self.validate()

    def set_gpg_widgets_sensitive(self, value):
        self.lb_key_type.set_sensitive(value)
        self.spn_key_length.set_sensitive(value)
        self.txt_password.set_sensitive(value)
        self.txt_password_confirm.set_sensitive(value)
        self.txt_email.set_sensitive(value)
        self.txt_name.set_sensitive(value)
        self.txt_comment.set_sensitive(value)
        self.txt_key_expiry.set_sensitive(value)


    def validate(self):
        key_expiry_parsed = False
        try:
            key_expiry = datetime.datetime.strptime(string.strip(self.txt_key_expiry.get_text()), "%Y%m%d")
            key_expiry_parsed = True
        except Exception, ex:
            self.frontend.builder.root_widget.debugln("Didn't parse date: " + str(ex))
            #TODO: alert user that their date doesn't parse
            pass


        if self.chk_disable_password.get_active() == True or \
                (self.txt_password.get_text() == self.txt_password_confirm.get_text() and \
                len(self.txt_password.get_text()) > 0 and \
                key_expiry_parsed == True and \
                key_expiry > datetime.datetime.now()):
            self.frontend.gui_set_sensitive("btn_forward", True)
        else:
            self.frontend.gui_set_sensitive("btn_forward", False)


