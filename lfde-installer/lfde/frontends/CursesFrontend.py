#!/usr/bin/python

import os
import sys
import os.path
import traceback

from consoul.Builder import Builder
from GenericFrontend import GenericFrontend

from cursespage.Welcome import Welcome
from cursespage.Luks import Luks
from cursespage.UsbKey import UsbKey
from cursespage.Unmount import Unmount
from cursespage.ConfirmUsbKey import ConfirmUsbKey
from cursespage.Format import Format
from cursespage.Gpg import Gpg
from cursespage.BootScheme import BootScheme
from cursespage.Commit import Commit
from cursespage.Finish import Finish


class CursesFrontend(GenericFrontend):
    def __init__(self, choices, backend):
        self.page_classes = [Welcome, Luks, UsbKey, Unmount, ConfirmUsbKey, \
                Format, Gpg, BootScheme, Commit, Finish]

        self.builder = Builder(init_curses=False)
        self.builder.add_from_file(os.path.join(sys.prefix, "share/lfde-installer/gui/curses/main.xml"))
        self.builder.connect_signals({"on_win_main_destroy" : self.quit,
                "on_btn_forward_clicked" : self.forward,
                "on_btn_back_clicked" : self.back,
                "on_btn_quit_clicked" : self.gui_quit })


        self.builder.add_from_file(os.path.join(sys.prefix, "share/lfde-installer/gui/curses/entropy.xml"))

        self.win_main = self.builder.get_object("win_main")
        self.lbl_step_title = self.builder.get_object("lbl_step_title")
        self.lbl_step = self.builder.get_object("lbl_step")
        self.btn_forward = self.builder.get_object("btn_forward")

        GenericFrontend.__init__(self, choices, backend)


    def gui_load_page(self, page):
        page_path = os.path.join(sys.prefix, "share", "lfde-installer", "gui", "curses", page.source)
        print "Loading: " + page_path
        self.builder.add_from_file(page_path, parent=self.steps)

    def gui_main_loop(self):
        clean = False

        try:
            self.builder.init_curses()
            self.win_main.show()
            self.builder.main()
        except Exception, ex:
            self.builder.cleanup()
            clean = True
            traceback.print_exc()
        finally:
            if clean == False:
                self.builder.cleanup()

    def gui_quit(self):
        self.builder.exit()
        self.quit()

    def gui_set_sensitive(self, name, value):
        self.builder.get_object(name).set_sensitive(value)

    def gui_set_title(self, title):
        self.lbl_step_title.set_text(title)

    def gui_display_page(self, number):
        self.steps.set_current_page(number)
        self.lbl_step.set_text("Page " + str(number + 1) + " of " + str(len(self.pages)))

    def gui_message_box(self, message):
        raise Exception("Not implemented yet")
