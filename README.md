# README

This repo is a collection of scripts to setup a waveshare GSM/GPRS/GNSS HAT with a SimCom SIM800 module
I connected the module to the raspberry pi running [Venus OS](https://github.com/victronenergy/venus) using the onboard USB to Serial converter. It would be nice to use the UART of the raspberry pi but that is already used for the console (and u-boot)
To avoid serial starter messing with the device i programmed a custom ID to the cp2102 converter [Programming Tools](https://www.silabs.com/community/interface/knowledge-base.entry.html/2016/11/04/cp210x_legacy_progra-zARf)
Next add a rule similar to [this](./gsm/gsm.rules)

## GSM

To connect to the mobile network a sim card is required. Research your APN on the internet. Put [gprs](./gsm/gprs) into */etc/pppd/peers/*

``` bash
# Establish connection
pppd call gprs
```

In order to setup gsm on boot put [rc.local](./gsm/rc.local) under */data/* and call [connect_gsm.sh](./gsm/connect_gsm.sh) in items

## GPS
In order to use the GPS it has to be enable by some at commands
``` bash
#Power on GPS
echo "AT+CGNSPWR=1" > /dev/ttyUSB0
sleep 1
#Get gps info once
echo "AT+CGNSINF" > /dev/ttyUSB0
sleep 1
#Activate continous (1s) NMEA 0138 messages
echo "AT+CGNSTST" > /dev/ttyUSB0
```

To get a Fix it might take a long while (+10 min) to improve that yo can use [assisted gps](./gps/agps.sh) and place a battery in the RTC

## GPS + GSM

tbd.

[![Built with Spacemacs](https://cdn.rawgit.com/syl20bnr/spacemacs/442d025779da2f62fc86c2082703697714db6514/assets/spacemacs-badge.svg)](http://spacemacs.org)
