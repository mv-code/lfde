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
from threading import Thread

class CommitThread(Thread):

    def __init__(self, tasks, task_complete_callback, all_complete_callback):
        Thread.__init__(self)

        self.tasks = tasks
        self.task_complete_callback = task_complete_callback
        self.all_complete_callback = all_complete_callback

    def run(self):

        i = 0
        for task in self.tasks:
            print "Running task: " + task.name
            task.run()
            self.task_complete_callback(i)
            i += 1

        self.all_complete_callback()

