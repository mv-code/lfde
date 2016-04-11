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
import re
import sys
import stat
import shutil
import subprocess

from CommitTask import CommitTask

class InitramfsCommit(CommitTask):
    name = "Update initramfs scripts"
    weight = 10

    def __init__(self, commit_page, choices, progress_callback):
        CommitTask.__init__(self, commit_page, choices, progress_callback)


    def run(self):
        if self.choices.distro == "ubuntu":
            perms = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH

            # load some more modules at boot
            print "Updating /etc/initramfs-tools/modules"
            modules_fh = open("/etc/initramfs-tools/modules", "a")
            modules_fh.write("sd_mod\nehci_hcd\nuhci_hcd\nohci_hcd\nusb_storage\nnls_cp437\nnls_iso8859_1\ndm-cryptaes\nsha256\nsha512\nblowfish\nloopcbc\nblkcipher\n")
            modules_fh.close()
            self.progress_callback(0.2)

            print "Installing gpg_cryptroot" 
            shutil.copyfile("/usr/share/lfde-tools/ubuntu/lfde-initramfs-hook", "/etc/initramfs-tools/hooks/lfde")
            os.chmod("/etc/initramfs-tools/hooks/lfde", perms)
            self.progress_callback(0.4)

            print "Writing crypto config"
            config_fh = open("/etc/initramfs-tools/conf.d/crypto", "w")
            config_fh.write("HOSTNAME=" + self.choices.hostname)
            config_fh.close()
            self.progress_callback(0.8)


            print "Updating initramfs"
            # for some strange reason this doesn't like being redirected
            initramfs_proc = subprocess.Popen(["update-initramfs", "-u", "-k", "all"], stdout=sys.stdout, stderr=sys.stderr)

            if initramfs_proc.wait() != 0:
                raise Exception("update-initramfs failed")

        elif self.commit_page.frontend.distro == "fedora":
            # install the dracut module
            shutil.copytree("/usr/share/lfde-tools/fedora/89lfde", "/usr/share/dracut/modules.d/89lfde")

            # we use dracut instead
            # simply replace the current initramfs
            # TODO: we should probably copy the initramfs for both fedora and ubuntu
            # so the user has an operational system if this doesn't work

            dracut_proc = subprocess.Popen(["dracut", "--force"], stdout=sys.stdout, stderr=sys.stderr)
            if dracut_proc.wait() != 0:
                raise Exception("Dracut failed")

