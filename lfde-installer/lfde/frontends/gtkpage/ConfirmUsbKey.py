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
from lfde.util.Pulser import Pulser
from lfde.util.ReadTester import ReadTester

class ConfirmUsbKey(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.title = "Confirm USB key selection"
        self.source = "confirm_usbkey.glade"
        self.root_object_name = "root_confirm_usbkey"
        self.read_tester = None
        self.pulser = None

        self.START_TEXT = "Start Test Read"
        self.STOP_TEXT = "Stop Test Read"

    def load_page(self):
        self.frontend.builder.connect_signals({"on_btn_test_read_toggled" : self.on_btn_test_read_toggled,
                "on_chk_confirm_drive_toggled" : self.on_chk_confirm_drive_toggled})
        self.btn_test_read = self.frontend.builder.get_object("btn_test_read")
        self.prg_test_read = self.frontend.builder.get_object("prg_test_read")
        self.chk_confirm_drive = self.frontend.builder.get_object("chk_confirm_drive")
        self.btn_test_read.set_label(self.START_TEXT)


    def page_enter(self):
        # set forward button to non-sensitive until user has confirmed
        # the drive is correct
        self.frontend.gui_set_sensitive("btn_forward", False)
        self.chk_confirm_drive.set_active(False)

    def page_leave(self):
        # kill any running read thread
        if self.read_tester != None:
            if self.read_tester.running == True:
                self.read_tester.stop()

        if self.pulser != None:
            self.pulser.stop()

    def unload_page(self):
        self.page_leave()

    def on_chk_confirm_drive_toggled(self, data):
        if self.chk_confirm_drive.get_active() == True:
            self.frontend.gui_set_sensitive("btn_forward", True)
        else:
            self.frontend.gui_set_sensitive("btn_forward", False)


    def on_btn_test_read_toggled(self, data):
        if self.btn_test_read.get_active() == True:
            # start the test read
            self.read_tester = ReadTester(self.frontend.choices.usb_key_device)
            self.pulser = Pulser(self.progress, self.done)
            self.read_tester.start()
            self.pulser.start()

            self.btn_test_read.set_label(self.STOP_TEXT)
        else:
            self.read_tester.stop()
            self.pulser.stop()
            self.btn_test_read.set_label(self.START_TEXT)

    def progress(self):
        gtk.threads_enter()
        self.prg_test_read.pulse()
        gtk.threads_leave()

    def done(self):
        gtk.threads_enter()
        self.prg_test_read.set_fraction(1.0)
        gtk.threads_leave()

