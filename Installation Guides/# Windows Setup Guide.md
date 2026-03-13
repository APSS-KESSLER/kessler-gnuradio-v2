# Windows Setup Guide

This guide serves for users trying to interface with GNU radio on a windows 10/11 device
This guide should hopefully take you through all the drivers needed to develop GNU radio 
to an APSS standard!

If there is an aspect missing to this or any of the other guides for the linux distros
please take the initiative and add a segment with what you've found and how you fixed 
the issue. 

The prerequisites for this are python >= 3.11

## Basic Installation

Windows has the easiest setup out of any of the distros making it a very interfaceable option
Simply go to the following website:

https://wiki.gnuradio.org/index.php/InstallingGR

And follow the instructions on this website in order to get started!
There shouldn't be any problems from here as Radioconda handles the installation process 
of the radiocompanion and should deal with a majority of the dependencies

## SoapyRTLSDR drivers

For our Reception graphs we make use of the RTL SDR USB Port
This is a USB-A dongle that slaps into a COM Port on your device.

Inorder to check that it has been recognised by your device use the Device Manager 

Then install the drivers here:
https://github.com/pothosware/SoapyRTLSDR

Then install osmo-sdr:
https://github.com/gqrx-sdr/gr-osmosdr

Then install gr satellites:

documentation: https://gr-satellites.readthedocs.io/en/latest/

Installation Repo: https://github.com/daniestevez/gr-satellites/tree/main/python
