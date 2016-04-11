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
import os.path
import subprocess
import tempfile

from lfde.util.Gpg import Gpg
from CommitTask import CommitTask
from lfde.util.EntropyGenerator import EntropyGenerator

class GpgCommit(CommitTask):
    name = "Key Generation"
    weight = 25

    def __init__(self, commit_page, choices, progress_callback):
        CommitTask.__init__(self, commit_page, choices, progress_callback)

    def run(self):
        #TODO : make it so we can just skip steps
        if self.choices.disable_password == True:
            self.progress_callback(1.0)
            return

        # start the interactive entropy input page
        self.commit_page.show_entropy_window()

        # start the entropy generator if the user wants it
        if self.choices.gpg_use_entropy_generator:
            print "Starting entropy generator"
            entropy_generator = EntropyGenerator()
            entropy_generator.start()
            print "Entropy generator running"


        try:
            home_dir = os.path.join(self.choices.mountpoint, ".gnupg")
            print "Creating GPG keyring in dir: " + home_dir
            gpg = Gpg()
            gpg.gen_key(home_dir, self.choices.gpg_name, self.choices.gpg_email, \
                    self.choices.gpg_key_type, self.choices.gpg_sub_key_type, \
                    self.choices.gpg_key_length, self.choices.gpg_password, \
                    self.choices.gpg_key_expiry_date)
        except Exception, ex:
            raise ex
        finally:
            if self.choices.gpg_use_entropy_generator:
                print "Stopping entropy generator"
                entropy_generator.stop()
            self.commit_page.hide_entropy_window()

        self.progress_callback(1.0)

