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

import os
import hashlib

class EntropyGenerator(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.running = False
        self.stopping = False


    def run(self):
        self.running = True

        # only scan safe dirs (not proc sys etc)
        scan_dirs = ["/bin", "/etc", "/home", "/lib", "/opt", "/root", "/sbin", "/usr"]
        while self.stopping == False:
            for scan_dir in scan_dirs:
                if self.stopping:
                    break

                for root, dirs, files in os.walk(scan_dir):
                    if self.stopping:
                        break

                    for file in files:
                        if self.stopping:
                            break


                        rel_path = os.path.join(root, file)
                        if os.path.isfile(rel_path) == False or \
                                os.path.islink(rel_path) == True or \
                                os.path.ismount(rel_path):
                            continue

                        m = hashlib.md5()
                        s = hashlib.sha256()

                        try:
                            # sha256 the file.
                            fh = open(rel_path, "r")
                            while self.stopping == False:
                                buf = fh.read(1024)
                                if not buf:
                                    break
                                s.update(buf)
                                m.update(buf)
                            fh.close()

                            s.hexdigest()
                            m.hexdigest()

                            #print "EntropyGenerator: " + s.hexdigest() + ": " + rel_path
                        except:
                            pass


        self.running = False
        self.stopping = False

    def stop(self):
        self.stopping = True

if __name__ == "__main__":
    e = EntropyGenerator()
    e.start()
