import pygtk
pygtk.require("2.0")
import gtk

import os
import sys
import os.path

from GenericFrontend import GenericFrontend

from gtkpage.Welcome import Welcome
from gtkpage.Debug import Debug
from gtkpage.Luks import Luks
from gtkpage.UsbKey import UsbKey
from gtkpage.Unmount import Unmount
from gtkpage.ConfirmUsbKey import ConfirmUsbKey
from gtkpage.Format import Format
from gtkpage.Gpg import Gpg
from gtkpage.BootScheme import BootScheme
from gtkpage.Commit import Commit
from gtkpage.Finish import Finish


class GtkFrontend(GenericFrontend):
    def __init__(self, choices, backend):
        self.page_classes = [Welcome, Luks, UsbKey, Unmount, ConfirmUsbKey, \
                Format, Gpg, BootScheme, Commit, Finish]

        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(sys.prefix, "share/lfde-installer/gui/gtk/main.glade"))
        self.builder.connect_signals({"on_win_main_destroy" : self.gui_quit,
                "on_btn_forward_clicked" : self.gui_forward,
                "on_btn_back_clicked" : self.gui_back,
                "on_btn_quit_clicked" : self.gui_quit })

        # allow our threads to work normally
        gtk.gdk.threads_init()

        self.win_main = self.builder.get_object("win_main")
        self.lbl_step_title = self.builder.get_object("lbl_step_title")

        self.builder.add_from_file(os.path.join(sys.prefix, "share/lfde-installer/gui/gtk/entropy.glade"))
        self.win_entropy = self.builder.get_object("win_entropy")
        self.lbl_step = self.builder.get_object("lbl_step")
        self.btn_forward = self.builder.get_object("btn_forward")

        GenericFrontend.__init__(self, choices, backend)

    def gui_load_page(self, page):
        page_path = os.path.join(sys.prefix, "share", "lfde-installer", "gui", "gtk", page.source)
        print "Loading: " + page_path
        self.builder.add_from_file(page_path)
        widget = self.builder.get_object(page.root_object_name)
        if widget == None:
            print "Your page must have an emelement called root_[pagename] to indicate which " + \
                    "element is the real root object"
            sys.exit(1)
        widget.reparent(self.steps)

    def gui_main_loop(self):
        self.win_main.show()
        gtk.main()

    def gui_back(self, data):
        self.back()

    def gui_forward(self, data):
        self.forward()

    def gui_set_sensitive(self, name, value):
        self.builder.get_object(name).set_sensitive(value)

    def gui_quit(self, data):
        self.quit()

        gtk.main_quit()

    def gui_set_title(self, title):
        self.lbl_step_title.set_text(title)

    def gui_display_page(self, number):
        self.steps.set_current_page(number)
        self.lbl_step.set_text("Page " + str(number + 1) + " of " + str(len(self.pages)))

    def gui_message_box(self, message):
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
                gtk.BUTTONS_NONE, message)
        dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        dialog.run()
        dialog.destroy()

