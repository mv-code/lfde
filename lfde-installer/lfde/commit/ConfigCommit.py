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
import os.path
from xml.dom.minidom import Document

from CommitTask import CommitTask

class ConfigCommit(CommitTask):
    name = "Write Config File"
    weight = 5

    def __init__(self, commit_page, choices, progress_callback):
        CommitTask.__init__(self, commit_page, choices, progress_callback)


    def run(self):

        # we should probably do this somewhere else
        doc = Document()
        lfde = doc.createElement("lfde")
        doc.appendChild(lfde)

        bootscheme = doc.createElement("bootscheme")
        bootscheme.appendChild(doc.createTextNode(self.choices.boot_scheme))
        lfde.appendChild(bootscheme)

        if os.path.exists("/etc/lfde") == False:
            os.makedirs("/etc/lfde")
        config_fh = open("/etc/lfde/config.xml", "w")
        config_fh.write(doc.toprettyxml())
        config_fh.close()

        self.progress_callback(1.0)
