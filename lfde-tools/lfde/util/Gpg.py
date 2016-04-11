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
import datetime
import tempfile
import subprocess

class Gpg:

    def encrypt_buffer(self, home_dir, email, buffer):
        cmd = ["gpg", "-q", "--homedir", home_dir, "--encrypt", "-r", email]
        print "Gpg cmd: " + str(cmd)
        stdout_data, stderr_data = subprocess.Popen(cmd, stdout=subprocess.PIPE, \
                stdin=subprocess.PIPE, stderr=subprocess.PIPE).communicate(input=buffer)

        print "GPG stderr: " + stderr_data

        return stdout_data



    def encrypt_buffer_what_was_i_thinking_version(self, home_dir, email, passphrase, buffer):
        out_fd_r, out_fd_w = os.pipe()
        in_fd_r, in_fd_w = os.pipe()
        err_fd_r, err_fd_w = os.pipe()
        #passphrase_fd_r, passphrase_fd_w = os.pipe()


        pid = os.fork()
        if pid:
            # we're the parent

            # we don't really need to replace our file handles
            # we can just use them

            gpg_out = os.fdopen(out_fd_w, "w")
            os.close(out_fd_r)

            gpg_in = os.fdopen(in_fd_r, "r")
            os.close(in_fd_w)

            gpg_err = os.fdopen(err_fd_r, "r")
            os.close(err_fd_w)

            cmd = ["gpg", "-q", "--homedir", home_dir, "--encrypt", "-r", email]
            #gpg_passphrase = os.fdopen(passphrase_fd_w, "w")
            #os.close(passphrase_fd_r)

            #gpg_passphrase.write(passphrase + "\n")
            #gpg_passphrase.close()
            #print "Written passphrase"

            gpg_out.write(buffer)
            gpg_out.close()

            print "Written buffer"

            # now read the results
            encrypted_buffer = gpg_in.read()
            errors = gpg_err.read()
            print "Errors: " + errors

            gpg_in.close()
            gpg_err.close()

            return encrypted_buffer

        else:
            # we're the child
            
            # replace stdin with input part of pipe
            os.dup2(out_fd_r, 0)
            os.close(out_fd_w)

            # replace stdout with output part of pipe
            os.dup2(in_fd_w, 1)
            os.close(in_fd_r)

            # replace stderr with error part of pipe
            os.dup2(err_fd_w, 2)
            os.close(err_fd_r)

            #os.dup2(passphrase_fd_r, 3)
            #os.close(passphrase_fd_w)

            os.close(out_fd_r)
            os.close(in_fd_w)
            os.close(err_fd_w)
            #os.close(passphrase_fd_r)

            # gpg command
            #os.execv("/usr/bin/gpg", ["gpg", "-q", "--homedir", home_dir, \
            #        "--passphrase-fd", "3", "--encrypt", "-r", email])
            os.execv("/usr/bin/gpg", ["gpg", "-q", "--homedir", home_dir, \
                    "--encrypt", "-r", email])



    def gen_key(self, home_dir, name, email, key_type, sub_key_type, key_length, passphrase, expire_date):

        cmd = ["gpg", "--batch", "--homedir", home_dir, "--gen-key"]

        gpg_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=sys.stderr)

        expire_date = datetime.datetime.strftime(expire_date, "%Y-%m-%d")
        gpg_proc.stdin.write("%echo starting\n")
        gpg_proc.stdin.write("Key-Type: " + key_type + "\n")
        gpg_proc.stdin.write("Key-Length:" + str(key_length) + "\n")
        gpg_proc.stdin.write("Subkey-Type: " + sub_key_type + "\n")
        gpg_proc.stdin.write("Subkey-Length:" + str(key_length) + "\n")
        gpg_proc.stdin.write("Name-Real: " + name + "\n")
        gpg_proc.stdin.write("Name-Email: " + email + "\n")
        gpg_proc.stdin.write("Expire-Date: " + expire_date + "\n")
        gpg_proc.stdin.write("Passphrase: " + passphrase + "\n")
        gpg_proc.stdin.write("%commit\n")
        gpg_proc.stdin.write("%echo done\n")

        gpg_proc.stdin.close()

        while True:
            char = gpg_proc.stdout.read(1)
            if not char:
                break
            print char,


if __name__ == "__main__":
    g = Gpg()
    sys.stdout.write(g.encrypt_buffer("/home/mark/gpg_test/home", "mark@mar", "blah", "This is a test text buffer"))

