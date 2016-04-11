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

class Page:
    def __init__(self, frontend):
        self.frontend = frontend
        self.backend = frontend.backend

        self.title = None
        self.source = None

    # abstract
    def page_leave(self):
        pass

    # abstract
    #TODO: name these consitently
    def unload_page(self):
        pass

    def hook_forward(self):
        return True

    def page_enter(self):
        pass
