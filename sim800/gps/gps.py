#!/usr/bin/python
# Filename: text.py
import serial
import time
import pynmea2
from at_lib import at_communicate, init_gps
import logging
from time import sleep




def main():
    with serial.Serial("/dev/ttyUSB0", 115200) as ser:
        logging.info("Preparing GPS")
        init_gps(ser)
        logging.info("Enter Main Loop")
        while True:

            try:
                line = ser.readline()
                msg = pynmea2.parse(line)
                if type(msg) is pynmea2.GGA:
                    logging.info("lat: {}; lon: {}".format(
                        msg.latitude, msg.longitude))
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
