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
import glob

class Luks:

    def test(self):
        print "Checking LUKS setup by opening lfde-test"
        cmd = ["cryptsetup", "luksOpen", root_device, "lfde-test"]
        cryptsetup_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

        cryptsetup_proc.stdin.write(self.txt_password.get_text())
        cryptsetup_proc.stdin.close()

        retcode = cryptsetup_proc.wait()

        if retcode == 0:
            self.lbl_ok.set_visible(True)
            self.lbl_not_ok.set_visible(False)
            self.frontend.gui_set_sensitive("btn_forward", True)
        elif retcode == 255:
            self.lbl_ok.set_visible(False)
            self.lbl_not_ok.set_visible(True)
            self.frontend.gui_set_sensitive("btn_forward", False)
        else:
            self.lbl_ok.set_visible(False)
            self.lbl_not_ok.set_visible(True)
            self.frontend.gui_set_sensitive("btn_forward", False)
            print "Unhandled cryptsetup return code: " + str(retcode)


        # now shut it
        cmd = ["cryptsetup", "luksClose", "lfde-test"]
        cryptsetup_proc = subprocess.call(cmd)



    def find_root_dev(self):
        """This basically reads crypttab and fstab to find out
           what the unencrypted root device is"""

        crypttab_fd = open("/etc/crypttab", "r")

        luks_devices = {}
        for line in crypttab_fd:
            line = line.strip()
            fields = line.split()

            # get rid of the UUID and convert it to a device node
            # if necessary
            if fields[1].find("UUID") != -1:
                fields[1] = os.path.join("/dev/disk/by-uuid", fields[1].replace("UUID=", ""))

            # first field is the encrypted device in /dev/mapper
            # second field is the underlying device
            luks_devices[fields[0]] = fields[1]


        crypttab_fd.close()

        # now look up the fstab
        fstab_fd = open("/etc/fstab", "r")

        mountpoints = {}
        for line in fstab_fd:
            line = line.strip()
            fields = line.split()

            if len(fields) < 2:
                continue

            # first field is device
            # second field is mountpoint
            mountpoints[fields[1]] = fields[0]

        

        fstab_fd.close()

        # now match the root device to the underlying device
        # this is not as easy as it sounds because there's not
        # just one way to do this.
        #
        # example 1:
        # */dev/sda3 (LVM PV) (LUKS FORMATTED)
        # /dev/mapper/luks-90b279b2-d71a-48f9-befb-305891da3d98 (LVM VG)
        # /dev/os-root (ext4 volume)
        #
        # example 2:
        # */dev/sda3 (LUKS FORMATTED)
        # /dev/mapper/crypt_sda3 (ext4 volume)
        #
        # example 3 (yes, I've seen this):
        # /dev/md0 (RAID, LVM PV, VG)
        # /dev/md1 (RAID, LVM PV, VG)
        # */dev/mapper/md_combined (LVM LV) (LUKS Formatted)
        # /dev/mapper/luks-90b279b2-d71a-48f9-befb-305891da3d98 (LVM VG)
        # /dev/os-root (ext4 volum)
        #
        # In each of the above, the * indicates the device we need
        # to detect
        #
        # There is a more efficient way of doing this, by working
        # the other way, but it would involve making rules
        # to handle the different types of device nodes.
        # for example, we have to handle sda5 different to md0 and
        # dm-1 because in sysfs sda5 is broken into sda/sda5
        # Annoying really... so we do it in reverse.  It's more
        # likely to cater for more scenarios I haven't thought of.

        # list /sys/block/dm-* until we find the root device
        root_dev = mountpoints["/"]
        root_dev_dm_name = root_dev.replace("/dev/mapper/", "")

        # find the first dm-* node
        # TODO: I'm pretty sure it will always be a dm device,
        # because LUKS creates a device mapper entry
        for dm_dir in glob.glob("/sys/block/dm-*"):
            dm_name_fh = open(os.path.join(dm_dir, "dm", "name"), "r")
            dm_name = dm_name_fh.read().strip()
            dm_name_fh.close()

            if dm_name == root_dev_dm_name:
                break


        while True:

            # otherwise we need to try the slave next
            slaves_dir = os.path.join(dm_dir, "slaves")
            slaves = os.listdir(slaves_dir)
            if len(slaves) > 1:
                raise Exception("More than one slave found, please report this as a bug")

            slave_dev = os.path.join("/dev/" + slaves[0])
            for enc_dev, und_dev in luks_devices.items():
                if os.path.samefile(slave_dev, und_dev):
                    return slave_dev
                    

            # ok, so we're not at the right node yet.  we enumerate the first
            # slave directory now
            dm_dir = os.path.join(slaves_dir, slaves[0])


if __name__ == "__main__":
    print Luks().find_root_dev()
