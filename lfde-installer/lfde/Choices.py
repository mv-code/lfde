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

class Choices:
    """This class contains the global configuration choices from the user.
       We share it between all the pages as some details need to be shared.
       For example, the device chosen for the USB key is probably one of the
       most shared variables, so we keep it in here.  We also keep it in here
       so we can marshall the object for debugging purposes"""

    def __init__(self):
        # define all variables here
        self.hostname = None
        self.usb_key_device = None
        self.usb_key_partition = None
        self.fs_type = None
        self.gpg_name = None
        self.gpg_email = None
        self.gpg_comment = None
        self.gpg_key_type = None
        self.gpg_sub_key_type = None
        self.gpg_key_length = None
        self.gpg_password = None
        self.gpg_key_expiry_date = None
        self.gpg_use_entropy_generator = None
        self.mountpoint = None
        self.boot_scheme = None
        self.username = None
        self.luks_old_key = None
        self.disable_password = None
