#!/usr/bin/python
import sys
import os
import serial
import select
import subprocess as sp
import logging

_default_device = '/dev/ttyUSB0'
_default_baudrate = 115200
_default_width = serial.EIGHTBITS
_default_parity = serial.PARITY_NONE
_default_stopbits = serial.STOPBITS_ONE
_default_xon = 0
_default_rtc = 0

_READ_ONLY = select.POLLIN | select.POLLPRI


def run(device=_default_device,
        baudrate=_default_baudrate,
        width=_default_width,
        parity=_default_parity,
        stopbits=_default_stopbits,
        xon=_default_xon,
        rtc=_default_rtc):
    ##### Serial port setup
    ttyS = serial.Serial(device, baudrate, width, parity, stopbits, 1, xon,
                         rtc)
    ttyS.timeout = 0  # Non-blocking

    ttyS.write("AT\r\n")
    data = ""
    while data != "OK\r\n":
        data = ttyS.readline()
        #logging.debug(data)
    number_of_slave_terminals = 1
    ##### PTYs setup
    pts = []
    for n in range(number_of_slave_terminals):
        master, slave = os.openpty()
        # Print slave names so others know where to connect
        print >> sys.stderr, 'MUX > fd: %d pty: %s' % (slave,
                                                       os.ttyname(slave))
        pts.append(master)

    ##### Poller setup
    poller = select.poll()
    poller.register(ttyS.fd, select.POLLIN | select.POLLPRI)
    for pt in pts:
        poller.register(pt, select.POLLIN | select.POLLPRI)

    ##### MAIN
    while True:

        events = poller.poll(500)

        for fd, flag in events:

            # fd has input
            if flag & (select.POLLIN | select.POLLPRI):
                # Data on serial
                if fd == ttyS.fd:
                    data = ttyS.read(80)
                    for pt in pts:
                        os.write(pt, data)

                # Data on other pty
                else:
                    ttyS.write(os.read(fd, 80))


if __name__ == "__main__":
    import optparse
    logging.basicConfig(level=logging.DEBUG)
    # Option parsing, duh
    parser = optparse.OptionParser()
    parser.add_option('-d',
                      '--device',
                      help='Serial port device',
                      dest='device',
                      default=_default_device)
    parser.add_option('-b',
                      '--baud',
                      help='Baud rate',
                      dest='baudrate',
                      type='int',
                      default=_default_baudrate)
    (opts, args) = parser.parse_args()

    run(device=opts.device, baudrate=opts.baudrate)
