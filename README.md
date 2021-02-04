# README

This repo is a collection of scripts to setup a waveshare GSM/GPRS/GNSS HAT with a SimCom SIM800 module
I connected the module to the raspberry pi running [Venus OS](https://github.com/victronenergy/venus) using the onboard USB to Serial converter. It would be nice to use the UART of the raspberry pi but that is already used for the console (and u-boot)
To avoid serial starter messing with the device i programmed a custom ID to the cp2102 converter [Programming Tools](https://www.silabs.com/community/interface/knowledge-base.entry.html/2016/11/04/cp210x_legacy_progra-zARf)
## GSM
To connect to the mobile network a sim card is required. Research your APN on the internet.


