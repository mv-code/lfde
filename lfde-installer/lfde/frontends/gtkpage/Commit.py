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
import sys
import subprocess

from ..Page import Page
from ...CommitThread import CommitThread

class Commit(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)

        self.title = "Install"
        self.source = "commit.glade"
        self.root_object_name = "root_commit"

        self.task_images = []
        self.finished = False
        self.task_count = 0

    def load_page(self):

        self.tbl_tasks = self.frontend.builder.get_object("tbl_tasks")
        self.prg_tasks = self.frontend.builder.get_object("prg_tasks")

        for task in self.frontend.backend.commit_tasks:
            self.gui_add_task(task)

    def page_enter(self):
        self.frontend.btn_forward.set_label("Install")
        self.frontend.gui_set_sensitive("btn_forward", True)

    def page_leave(self):
        self.frontend.btn_forward.set_label("Forward")

    def hook_forward(self):
        if self.finished == False:
            self.frontend.gui_set_sensitive("btn_back", False)
            self.frontend.gui_set_sensitive("btn_forward", False)

            self.frontend.backend.commit(self.frontend.choices, self)

        else:
            return True

    def set_progress(self, fraction):
        gtk.gdk.threads_enter()
        self.prg_tasks.set_fraction(fraction)
        gtk.gdk.threads_leave()

    def task_complete(self, id):
        gtk.gdk.threads_enter()
        self.task_images[id].show()
        gtk.gdk.threads_leave()

    def all_complete(self):
        gtk.gdk.threads_enter()
        self.finished = True
        self.prg_tasks.set_fraction(1.0)
        self.frontend.gui_set_sensitive("btn_forward", True)
        self.frontend.backend.main.undirect_output()

        self.frontend.btn_forward.set_label("Forward")
        self.frontend.forward()

        gtk.gdk.threads_leave()


    def gui_add_task(self, task):
        label = gtk.Label(task.name)
        label.set_alignment(0.0, 0.0)
        row = self.task_count + 1
        col = 0  
        # col_left_attach, col_right_attach, row_top_attach, row_bottom_attach
        self.tbl_tasks.attach(label, col, col + 1, row, row + 1)
        label.show()

        col = 1 
        image = gtk.Image() 
        image.set_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
        image.set_alignment(0.0, 0.0)
        self.tbl_tasks.attach(image, col, col + 1, row, row + 1)
        self.task_images.append(image)

        self.task_count += 1



    def show_entropy_window(self):
        gtk.gdk.threads_enter()
        self.frontend.win_entropy.show()
        self.frontend.win_entropy.set_keep_above(True)
        gtk.gdk.threads_leave()

    def hide_entropy_window(self):
        gtk.gdk.threads_enter()
        self.frontend.win_entropy.set_keep_above(False)
        self.frontend.win_entropy.hide()
        gtk.gdk.threads_leave()

