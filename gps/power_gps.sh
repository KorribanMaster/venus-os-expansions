#!/bin/bash
#Power on GPS
sleep 1
echo "AT+CGNSPWR=1" > /dev/ttyUSB0
sleep 1
#Send EPO file to GPS
echo "AT+CGNSAID=31,1,1" > /dev/ttyUSB0
sleep 1
echo "AT+CGNSTST=1" > /dev/ttyUSB0
