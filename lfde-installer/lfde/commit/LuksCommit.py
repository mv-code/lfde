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
import sys
import string
import subprocess

from lfde.util.Gpg import Gpg
from lfde.util.Luks import Luks

from CommitTask import CommitTask

class LuksCommit(CommitTask):
    name = "Configure LUKS"
    weight = 10

    def __init__(self, commit_page, choices, progress_callback):
        CommitTask.__init__(self, commit_page, choices, progress_callback)


    def run(self):
        # make a directory for keys
        crypto_dir = os.path.join(self.choices.mountpoint, ".crypto")
        if os.path.exists(crypto_dir) == False:
            os.mkdir(crypto_dir)

        self.progress_callback(1.0)

        print "Generating raw LUKS key"
        key = self.generate_key()

        # now gpg encrypt the key
        if self.choices.disable_password == False:
            print "GPG encrypting the LUKS key"
            home_dir = os.path.join(self.choices.mountpoint, ".gnupg")
            gpg = Gpg()
            encrypted_key = gpg.encrypt_buffer(home_dir, self.choices.gpg_email, key)

            print "Writing GPG enrypted LUKS key to USB key"
            # write the key to the users crypto dir
            host_key_path = os.path.join(crypto_dir, self.choices.hostname + ".key.enc")
            host_key_fd = open(host_key_path, "w")
            host_key_fd.write(encrypted_key)
            host_key_fd.close()
        else:
            # store the key as is
            key_fh = open(os.path.join(crypto_dir, self.choices.hostname + ".key"), "w")
            key_fh.write(key)
            key_fh.close()


        root_device = Luks().find_root_dev()

        # now add the key to the luks Header
        # TODO: unfortunately cryptsetup doesn't support file descriptors
        # like GPG. So we need to save either the new key or the old key
        # to disk.  We choose the old key as it's obviously not as important
        # TODO:we can probably fix this with FIFOs or something.  UGLY.

        old_key_path = os.path.join("/dev/shm", "old.key")
        old_key_fd = open(old_key_path, "w")
        old_key_fd.write(self.choices.luks_old_key)
        old_key_fd.close()

        # we try to add the key up to 10 times as sometimes cryptsetup fails
        print "Adding new lfde key to LUKS"
        success = False
        for i in range(10):
            print "Attempt " + str(i)
            cmd = ["cryptsetup", "luksAddKey", "-d", old_key_path, root_device]
            cryptsetup_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=sys.stderr, stdout=sys.stdout)

            cryptsetup_proc.stdin.write(key)
            cryptsetup_proc.stdin.close()

            if cryptsetup_proc.wait() == 0:
                success = True
                break

        if success == False:
            raise Exception("luksAddKey failed")
        else:
            print "Success!"


        print "Removing old luks key"
        success = False
        for i in range(10):
            print "Attempt " + str(i)
            cmd = ["cryptsetup", "luksKillSlot", root_device, "0"]
            cryptsetup_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=sys.stderr, stdout=sys.stdout)

            cryptsetup_proc.stdin.write(key)
            cryptsetup_proc.stdin.close()

            if cryptsetup_proc.wait() == 0:
                success = True
                break

        if self.choices.distro == "ubuntu":
            print "Writing crypttab"
            # now update the crypttab
            # use line from above
            line = line.rstrip()
            crypttab_fh = open("/etc/crypttab", "w")
            crypttab_fh.write(line + ",keyscript=/usr/bin/cryptgetpw")
            crypttab_fh.close()



    def generate_key(self):
        rand_fh = open("/dev/urandom", "r")

        key = ""
        while len(key) != 32:
            byte = rand_fh.read(1)

            if byte != "\n" and byte != "\0":
                key += byte

        rand_fh.close()

        return key

