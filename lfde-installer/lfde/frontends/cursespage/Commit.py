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
from ...CommitThread import CommitThread

class Commit(Page):
    def __init__(self, frontend):
        Page.__init__(self, frontend)
        self.backend = self.frontend.backend

        self.title = "Install"
        self.source = "commit.xml"

        self.finished = False
        self.task_count = 0
        self.task_y_offset = 3

    def load_page(self):

        self.prg_tasks = self.frontend.builder.get_object("prg_tasks")
        self.root_commit = self.frontend.builder.get_object("root_commit")

        # load entropy window
        self.root_entropy = self.frontend.builder.get_object("root_entropy")
        self.txt_random = self.frontend.builder.get_object("txt_random")

        self.frontend.builder.connect_signals({"on_txt_random_changed" : self.on_txt_random_changed})

        y_pos = self.task_y_offset
        for task in self.backend.commit_tasks:
            label = self.frontend.builder.render_label(None, self.root_commit)
            label.x = 0
            label.y = y_pos
            label.width = 40
            label.height = 1
            label.text = task.name
            #label.show()
            y_pos += 1

    def page_enter(self):
        self.frontend.btn_forward.set_label("Install")
        self.frontend.gui_set_sensitive("btn_forward", True)

    def page_leave(self):
        self.frontend.btn_forward.set_label("Forward")

    def on_txt_random_changed(self):
        if len(self.txt_random.get_text()) + 2 > self.txt_random.width:
            self.txt_random.set_text("")

    def hook_forward(self):
        if self.finished == False:
            self.frontend.gui_set_sensitive("btn_back", False)
            self.frontend.gui_set_sensitive("btn_forward", False)

            self.backend.commit(self.frontend.choices, self)

        else:
            return True

    def set_progress(self, fraction):
        self.prg_tasks.set_value(fraction)

    def task_complete(self, index):
        # print a tick
        label = self.frontend.builder.render_label(None, self.root_commit)
        label.x = 50
        label.y = self.task_y_offset + index
        label.width = 6
        label.height = 1
        label.text = "Done"
        label.show()

    def all_complete(self):
        self.finished = True
        self.prg_tasks.set_value(1.0)
        self.frontend.gui_set_sensitive("btn_forward", True)
        self.backend.main.close_log()

        self.frontend.gui_set_sensitive("btn_back", False)
        self.frontend.gui_set_sensitive("btn_forward", False)
        self.frontend.forward()


    def show_entropy_window(self):
        self.root_entropy.show()

    def hide_entropy_window(self):
        self.root_entropy.hide()

        #TODO: make the framework redraw the main window
        self.frontend.win_main.show()
