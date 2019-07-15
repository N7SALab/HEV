"""
Scan, Own, Find (SOF) everything wireless on the 2.5 and 5.0 GHz bandwidth

Bluetooth bandwidth support will be added in future versions
"""

import re
import os
import sys
import subprocess

from subprocess import STDOUT

from core.helpers.sanitation import Sanitation


class Wireless:
    """
    Enumerate system wireless capabilities
    """

    def __init__(self):
        self.platform = sys.platform
        self.devices = self._devices()
        self.wireless_devices = self._wireless_devices()

    def _wireless_devices(self):
        """These are definitely your wireless devices that you have available for you to use
        Have fun

        :return:
        """

        wireless_devices = []
        devices = self.devices

        for device in devices:
            for console_line in subprocess.check_output('iwconfig'.split(), stderr=STDOUT).splitlines():
                if re.findall('^' + device, console_line.decode()) and not re.findall('no wireless extensions',
                                                                                      console_line.decode()):
                    # TODO: Add support for multiple wireless cards in future
                    # Create a list of multiple wireless cards and let the user know

                    # TODO: Get wireless device type (a,b,g,n,ac,ad)
                    # Depending on the wireless capabilities of the card, pick the one with the most capabilities
                    # Use that card to scan on the frequency that none others can. Then use the other cards to
                    # scan for the other frequencies

                    # TODO: Get wireless device modes that are available
                    # If more than one wireless devices, find out what modes it can run in (managed, monitor, master)
                    # Use card with master mode as an AP

                    wireless_devices.append(str(device).strip())

        if wireless_devices:
            return wireless_devices
        else:
            raise Exception('No wireless devices found: ', devices)

    def _devices(self):
        """
        Return either a list of all wireless devices or the best wireless device to use on this excursion

        TODO: Get system wireless devices
        Using iw, and iwconfig to enumerate the wireless devices of the system
        """

        devices = []

        # TODO: Get wireless devices from iwconfig
        # These should be the network devices that the system knows based on iwconfig

        # TODO: Get wireless devices from ifconfig
        # Possibly match against the devices found in ifconfig

        # TODO: Get wireless devices from dmesg
        # Possibly match what the boot log shows

        # TODO: Get wireless devices from lspci
        # Maybe something here

        # /sys/class/net/
        path = '/sys/class/net/'

        if os.path.exists(path):
            devices.extend(os.listdir(path))

        return Sanitation.dedup(devices)

    def _sonar(self):
        """
        Get all of the wireless signals around you and the area that you're in
        Let the owning begin

        TODO: Find out all of the wireless stations, bssids around
        The list of all the stations and bssids will be used to create a database, a graph database
        """

        return
