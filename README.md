# README

This repo is a collection of expansions for the [venus-os](https://github.com/KorribanMaster/venus) from victronenergy running on a raspberry pi. As i only have a raspberry pi 2 everything is only tested on this device.
Detailed descriptions about required changes and installation are inside the respective folders.

## sim800

The [sim800](https://www.waveshare.com/wiki/SIM800C_GSM/GPRS_HAT) raspberry pi hat from waveshare was my first shot at adding gsm+gps to the venus os. However due too the single serial interface i only got either gsm or gps working never both at the same time


## sim7600

The [sim7600](https://www.robotshop.com/de/de/4g-3g2ggsmgprsgnss-hat-fur-raspberry-pi-europa-so-w-asien-afrika.html)  raspberry pi hat from waveshare is fully functional and integrated in venus os with both gsm/4g and gps working with full integration into the gui

## ads1115

The ads1115 is an adc with 4 channels atached to the i2c interface. The goal would be to integrate it as tank/temperature sensor into the venus gui

## relay

This makes up to four relays available in the gui to control via the raspberry py gpios



# General Notes 
## Software update
When venus os is updated the rootfs is overwritten and all changes are lost. This could be prevented by putting them on /data and make an installer script hook run by /data/rc.local

## Interesting links

* [Display Setup](https://github.com/kwindrem/RpiDisplaySetup)
* [Installing + various notes on modifikations](https://github.com/victronenergy/venus/wiki/raspberrypi-install-venus-image)
* [SSH and persiting changes](https://www.victronenergy.com/live/ccgx:root_access)
* [Various setup information](https://github.com/aaronsb/victronvenussupport)

[![Built with Spacemacs](https://cdn.rawgit.com/syl20bnr/spacemacs/442d025779da2f62fc86c2082703697714db6514/assets/spacemacs-badge.svg)](http://spacemacs.org)
