# lfde.org

# Getting Started With Version 0.3

Installing LFDE has become a lot easier with the introduction of a GUI based installer. Release Notes This initial release comes with a few caveats and we're working on them:

*   Version 0.3 is compatible with Ubuntu Lucid (10.04) and Maverick (10.10)
*   You can only use one USB key per system (this will change with the next release)

## Install Ubuntu Alternate

You need to install your Ubuntu system with the alternate installer or the server installer. You can find an ISO image of the alternate installer by going to any of the Ubuntu mirrors.

Select the alternate iso that is suitable for your system. For example:

*   ubuntu-10.10-alternate-amd64.iso
*   ubuntu-10.10-alternate-i386.iso

When you install your system using the alternate or server installer, choose the option to encrypt your system. The LFDE installer needs this to work.

We use the encryption options to set up a basic encrypted system without the USB key or GPG protection. The LFDE installer needs to be run after the system is installed. It then modifies the system to boot more securely with the USB key.

## Add the LFDE APT Repository

Add the following line to /etc/apt/sources.list depending on your version of Ubuntu:

<table border="1">

<tbody>

<tr>

<th>Version:</th>

<th>Line:</th>

</tr>

<tr>

<td>Lucid Lynx (10.04):</td>

<td>`deb http://lfde.org/ubuntu lucid main`</td>

</tr>

<tr>

<td>Maverick Meercat (10.10):</td>

<td>`deb http://lfde.org/ubuntu maverick main`</td>

</tr>

</tbody>

</table>

## Add the LFDE GPG Key

`wget http://lfde.org/gpg.asc -O - | apt-key add -`

## Update APT

`sudo apt-get update`

## Install LFDE

Open up terminal by clicking:

`Applications -> Accessories -> Terminal`

## Install LFDE

`sudo apt-get install lfde-installer`

## Run the installer:

`sudo lfde-install`

Follow the steps

Now follow the installer steps and you should hopefully end up with a USB key protected Ubuntu installation. Be sure to change your BIOS to boot from USB if you choose to boot from USB. This is the most secure way the LFDE system works.

