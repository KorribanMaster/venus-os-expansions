# devicetree overlay
get [dts](https://github.com/raspberrypi/linux/blob/rpi-4.9.y/arch/arm/boot/dts/overlays/ads1115-overlay.dts) from upstream rpi project
`dtc -I dts -O dtb -o ads1115-overlay.dtb ads1115-overlay.dts`
copy dtb to /u-boot/overlays
add the following in a single line to the existing line in /u-boot/cmdline.txt
if a dtparam= or dtoverlay= already exists add them as a comma seperated list (no space)
u-boot will only pars the firs line that is not a comment
```
#turn on i2c_arm bus
dtoverlay=ads1115 dtparam=i2c_arm=on,i2c_arm_baudrate=400000,cha_enable,chb_enable,chc_enable,chd_enable
```
# manually load devicetree file 

```bash
mkdir /sys/kernel/config/device-tree/overlays/ads1115
cat /u-boot/overlays/ads1115-overlay.dtb > /sys/kernel/config/device-tree/overlays/ads1115/dtbo
```
# Using the adc values

The adc values can be read from /sys/bus/i2c/devices/1-0048/in{4-7}_input_

Getting the values into the dbus the [dbus-adc](https://github.com/victronenergy/dbus-adc) package would be a convenient starting point. Possibly one only has to replace the adc_read method in [adc.c](https://github.com/victronenergy/dbus-adc/blob/master/software/src/adc.c)
