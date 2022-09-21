#!/bin/bash
set -e
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
RELAY_QML_FILE=/opt/victronenergy/gui/qml/PageSettingsRelay.qml
GPIO_LIST_FILE=/etc/venus/gpio_list
SIM7600_RULES_FILE=/etc/udev/rules.d/sim7600.rules
function backup_file() {
    FILE=$1
    if [ -f "$FILE" ]; then
        echo "$FILE exists. Making backup"
        mv $FILE $FILE.bak
    fi
}
echo "Venos OS Expansion installer"
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
mv sim7600/sim7600.rules $SIM7600_RULES_FILE
udevadm control --reload-rules && udevadm trigger
