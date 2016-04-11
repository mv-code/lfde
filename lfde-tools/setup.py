#!/usr/bin/python

# This file has been generated automatically by mksetup.py
# https://mknowles.com.au/mksetup

from distutils.core import setup

# data files
data_files = []
data_files.append(('/usr/share/lfde-tools/fedora/89lfde', ['data/share/fedora/89lfde/check','data/share/fedora/89lfde/crypt-cleanup.sh','data/share/fedora/89lfde/parse-crypt.sh','data/share/fedora/89lfde/cryptroot-ask-lfde.sh','data/share/fedora/89lfde/69-lfde.rules','data/share/fedora/89lfde/install','data/share/fedora/89lfde/cryptgetpw','data/share/fedora/89lfde/installkernel']))
data_files.append(('/usr/share/lfde-tools/ubuntu', ['data/share/ubuntu/lfde-initramfs-hook']))
data_files.append(('/usr/share/lfde-tools', []))


setup(
    author_email='mark@lfde.org',
    url='https://lfde.org',
    version='1.1',
    name='lfde-tools',
    author='Mark Knowles',
    packages=['lfde','lfde.util'],
    scripts=['scripts/lfde-sync','scripts/cryptgetpw'],
    data_files=data_files
)
