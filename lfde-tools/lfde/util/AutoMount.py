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

from KillAll import KillAll

class AutoMount:

    def inhibit(self):
        KillAll().killall("/usr/lib/gvfs/gvfs-gdu-volume-monitor")

        #old ways that used to work, yes this is a shambles
        #gclient = gconf.client_get_default()
        #gval = gconf.Value(gconf.VALUE_BOOL)
        #gval.set_bool(False)
        #gclient.set('/desktop/gnome/volume_manager/automount_media', gval)
        #gclient.set('/desktop/gnome/volume_manager/automount_drives', gval)
        #gclient.set('/apps/nautilus/desktop/volumes_visible', gval)
        #gclient.set('/apps/nautilus/preferences/media_automount', gval)
        #gclient.set('/apps/nautilus/preferences/media_automount_open', gval)
        #gval.set_bool(True)
        #gclient.set('/apps/nautilus/preferences/media_autorun_never', gval)

    def restore(self):
        # the automount stuff survives reboot now, so don't worry
        pass
