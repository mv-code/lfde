import os
import re
import sys
import shutil
import subprocess
from distutils.core import setup

# get the revision number
#output = subprocess.Popen(["svn", "info"], stdout=subprocess.PIPE).communicate()[0]
#m = re.search(r"Revision:\s*(\d+)", output)
#if m == None:
#    print "I can't seem to determine the SVN revision number.  Exiting"
#    sys.exit(1)
#
#revision = "r" + m.group(1)

revision = "r1234"

def find_data_files(dest, subdir, a):
    r = []

    for file in os.listdir(subdir):
        rel_file = os.path.join(subdir, file)
        if file != ".svn":
            if os.path.isdir(rel_file):
                find_data_files(os.path.join(dest, file), rel_file, a)
            else:
                r.append(rel_file)

    a.append((dest, r))


data_files = []
find_data_files("share/lfde-installer", "data/share", data_files)


setup(
        name='lfde-installer',
        version=revision,
        author='Mark Knowles',
        author_email='mark@lfde.org',
        url='https://lfde.org',
        packages=['lfde', 'lfde.frontends', 'lfde.frontends.cursespage', 'lfde.frontends.gtkpage', 'lfde.commit'],
        scripts=['scripts/lfde-install'],
        data_files=data_files)

