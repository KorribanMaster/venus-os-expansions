#!/usr/bin/python
# Filename: text.py
import serial
import time
import pynmea2
from at_lib import at_communicate
import logging
from time import sleep
from dbusgpsservice import DbusGpsService

def main():
    at_list=[
    ["ATE0", None]
    ,["AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"", None] #Set bearer parameter
    ,["AT+SAPBR=3,1,\"APN\",\"INTERNET.T-MOBILE\"", None] #Set bearer context
    ,["AT+SAPBR=1,1", None] #Active bearer context
    ,["AT+SAPBR=2,1", "+SAPBR"] #Read NTP server and time zone parameter
    ,["AT+CNTPCID=1", None]
    ,["AT+CNTP", "+CNTP"] #Read local time
    ,["AT+CNTP?","+CNTP"] #Synchronize Network Time to local
    ,["AT+CCLK?", "+CCLK"] #Download EPO File
    ,["AT+FTPSERV=\"116.247.119.165\"", None]#Set FTP user name
    ,["AT+FTPUN=\"customer\"", None]#Set FTP password
    ,["AT+FTPPW=\"111111\"", None]#Set download file name
    ,["AT+FTPGETNAME=\"MTK3.EPO\"", None]#Set Download file path
    ,["AT+FTPGETPATH=\"/\"", None]#Download data to local buffer
    ,["AT+FTPEXTGET=1", "+FTPEXTGET"]#save data to local disk as EPO file
    ,["AT+FTPEXTGET=4,\"epo\"", "+FTPEXTGET"]#List Directories/Files
    ,["AT+CGNSCHK=3,1", "+CGNSCHK"]#Power on GPS
    ,["AT+CGNSPWR=1", None]#Send EPO file to GPS
    ,["AT+CGNSAID=31,1,1", None] #"+CGNSAID"]
    ,["AT+CGNSTST=1", None]]
    at_list=[
    ["AT+CGNSPWR=1", None]#Send EPO file to GPS
    ,["AT+CGNSTST=1", None]]
    with serial.Serial("/dev/ttyUSB0",115200) as ser:
        logging.info("Preparing GPS")
        for item in at_list:
            at_communicate(ser,item[0], item[1])
            sleep(0.1)
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
            })

        logging.info('Connected to dbus, and switching over to seraial driven mode')
        logging.info("Enter Main Loop")
        while True:

            try:
                line = ser.readline()
                msg = pynmea2.parse(line)
                if type(msg) is pynmea2.GGA:
                    logging.info("lat: {}; lon: {}".format(msg.latitude, msg.longitude))
                    gps_output.update_position(msg.latitude, msg.longitude)
                    #gps_output._update()
            except serial.SerialException as e:
                logging.error('Device error: {}'.format(e))
                break
            except pynmea2.ParseError as e:
                logging.warning('Parse error: {}'.format(e))
                continue


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
