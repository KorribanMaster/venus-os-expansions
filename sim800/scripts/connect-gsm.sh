#!/bin/sh
#kill victron services which intefer with ppp
rm -f /dev/serial-starter/ttyUSB0
svc -d /service/*.ttyUSB0
#power gsm module
echo "4" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio4/direction
echo "0" > /sys/class/gpio/gpio4/value
sleep 2
echo "1" > /sys/class/gpio/gpio4/value
#start pppd in backround
nohup pppd call gprs >/dev/null 2>&1 &
