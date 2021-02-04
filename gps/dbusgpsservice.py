#!/usr/bin/env python

"""
A class to put a gps service on the dbus, according to victron standards. It is used to put gps data for other processes that rely on the
dbus. 
"""
import gobject
import platform
import argparse
import logging
import sys
import os
import serial
import pynmea2
from at_lib import at_communicate, init_gps
from time import sleep

# our own packages
sys.path.insert(1, os.path.join(os.path.dirname(__file__), './ext'))
from vedbus import VeDbusService



class DbusGpsService:
    def __init__(self, servicename, deviceinstance, paths, productname='SIM868', connection='GPS'):
        self._dbusservice = VeDbusService(servicename)
        self._paths = paths

        logging.debug("%s /DeviceInstance = %d" % (servicename, deviceinstance))

        # Create the management objects, as specified in the ccgx dbus-api document
        self._dbusservice.add_path('/Mgmt/ProcessName', __file__)
        self._dbusservice.add_path('/Mgmt/ProcessVersion', 'Unkown version, and running on Python ' + platform.python_version())
        self._dbusservice.add_path('/Mgmt/Connection', connection)

        # Create the mandatory objects
        self._dbusservice.add_path('/DeviceInstance', deviceinstance)
        self._dbusservice.add_path('/ProductId', 0)
        self._dbusservice.add_path('/ProductName', productname)
        self._dbusservice.add_path('/FirmwareVersion', 0)
        self._dbusservice.add_path('/HardwareVersion', 0)
        self._dbusservice.add_path('/Connected', 1)

        for path, settings in self._paths.iteritems():
            self._dbusservice.add_path(
                path, settings['initial'], writeable=True, onchangecallback=self._handlechangedvalue)
        self.ser = serial.Serial("/dev/ttyUSB0", 115200)
        self.ser.timeout = 0
        self.ser.flushInput()

        init_gps(self.ser)
        gobject.timeout_add(1000, self.update_position)

    def update_position(self):
        num_waiting = self.ser.inWaiting()
        while num_waiting > 0:
            try:
                line = self.ser.readline()
                msg = pynmea2.parse(line)
                if type(msg) is pynmea2.GGA:
                    logging.info("lat: {}; lon: {}".format(
                        msg.latitude, msg.longitude))
                    self._dbusservice["/Position/Latitude"] = msg.latitude
                    self._dbusservice["/Position/Longtitude"] = msg.longitude
            except serial.SerialException as e:
                logging.error('Device error: {}'.format(e))
                break
            except pynmea2.ParseError as e:
                logging.warning('Parse error: {}'.format(e))
                continue
            num_waiting = self.ser.inWaiting()
        return True

    def _update(self):
        for path, settings in self._paths.iteritems():
            if 'update' in settings:
                self._dbusservice[path] = self._dbusservice[path] + settings['update']
                logging.debug("%s: %s" % (path, self._dbusservice[path]))
        return True

    def _handlechangedvalue(self, path, value):
        logging.debug("someone else updated %s to %s" % (path, value))
        return True # accept the change


# === All code below is to simply run it from the commandline for debugging purposes ===

# It will created a dbus service called com.victronenergy.pvinverter.output.
# To try this on commandline, start this program in one terminal, and try these commands
# from another terminal:
# dbus com.victronenergy.pvinverter.output
# dbus com.victronenergy.pvinverter.output /Ac/Energy/Forward GetValue
# dbus com.victronenergy.pvinverter.output /Ac/Energy/Forward SetValue %20
#
# Above examples use this dbus client: http://code.google.com/p/dbus-tools/wiki/DBusCli
# See their manual to explain the % in %20

def main():
    logging.basicConfig(level=logging.DEBUG)

    from dbus.mainloop.glib import DBusGMainLoop
    # Have a mainloop, so we can send/receive asynchronous calls to and from dbus
    DBusGMainLoop(set_as_default=True)

    gps_output = DbusGpsService(
        servicename='com.victronenergy.gps',
        deviceinstance=0,
        paths={
            '/Position/Latitude': {'initial': 66.3, 'update': 0},
            '/Position/Longtitude': {'initial': 67.3, 'update': 0},
            '/Speed': {'initial': 0, 'update': 0},
            '/Course': {'initial': 0, 'update': 0},
            '/Altitude': {'initial': 0, 'update': 0},
            '/NrOfSatelites': {'initial': 1, 'update': 0},
            '/Fix': {'initial': 1, 'update': 0},
            '/Nonupdatingvalue/UseForTestingWritesForExample': {'initial': None},
            '/DbusInvalid': {'initial': None}
        })

    logging.info('Connected to dbus, and switching over to gobject.MainLoop() (= event based)')
    mainloop = gobject.MainLoop()
    mainloop.run()


if __name__ == "__main__":
    main()


