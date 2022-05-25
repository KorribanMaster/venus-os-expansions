# Readme

To enable two additional manual relays in the GUI
1. adjust the [gpio_list](./gpio_list) file on the runninng venus like in the example file in this repo (make sure the pins fit your design). On the venus os the file is located at /etc/venus/gpio_list
2. copy [PageSettingsRelayAdditionalManualSwitches.qml](./PageSettingsRelayAdditionalManualSwitches.qml) to /opt/victronenergy/gui/qml/PageSettingsRelay.qml
