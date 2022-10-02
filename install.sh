#!/bin/bash
set -e
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
RELAY_QML_FILE=/opt/victronenergy/gui/qml/PageSettingsRelay.qml
GPIO_LIST_FILE=/etc/venus/gpio_list
SIM7600_RULES_FILE=/etc/udev/rules.d/simcom.rules
RC_LOCAL_FILE=/data/rc.local
function backup_file() {
    FILE=$1
    if [ -f "$FILE" ]; then
        echo "$FILE exists. Making backup"
        mv $FILE $FILE.bak
    fi
}
echo "Venus OS Expansion installer"
echo "Setting up relays"
backup_file $RELAY_QML_FILE
backup_file $GPIO_LIST_FILE
echo "Patching GUI"
cp $SCRIPT_DIR/relay/PageSettingsRelayAdditionalManualSwitches.qml $RELAY_QML_FILE
echo "Settting up GPIOs"
cp $SCRIPT_DIR/relay/gpio_list $GPIO_LIST_FILE
echo "Setting up SIM7600"
backup_file $SIM7600_RULES_FILE
opkg install dbus-modem gps-dbus
# Check if sim7600 is in correct usbmode

if lsusb | grep 1e0e:9011; then
    echo "Modem SIM7600 is in wrong configuration. Attempting to fix this. See Readme if script fails afterwards"
    echo "AT+CUSBPIDSWITCH=9001,1,1\r\n" > /dev/ttyUSB3
    sleep 30
fi
if lsusb | grep 1e0e:9001; then
    echo "All good"
else
    echo "Fix not succesfull please see readme for ideas on further troubleshooting"
fi

cp sim7600/sim7600.rules $SIM7600_RULES_FILE
udevadm control --reload-rules && udevadm trigger

echo "Setting up ADC"
cp $SCRIPT_DIR/ads1115/ads1115-overlay.dtb /u-boot/overlays

echo "See README for further setup of ads1115 which is not yet automated"

echo "Setting up /data/rc.local to persist changes"
backup_file $RC_LOCAL_FILE
cp $SCRIPT_DIR/rc.local $RC_LOCAL_FILE
touch /etc/venus-os-expansions
echo "Installation has finished. Please reboot"
