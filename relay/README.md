# Readme

## Software
Requires ssh access
To enable two additional manual relays in the GUI
1. adjust the [gpio_list](./gpio_list) file on the runninng venus like in the example file in this repo (make sure the pins fit your design). On the venus os the file is located at /etc/venus/gpio_list
2. copy [PageSettingsRelayAdditionalManualSwitches.qml](./PageSettingsRelayAdditionalManualSwitches.qml) to /opt/victronenergy/gui/qml/PageSettingsRelay.qml
 This can be done like this
 ```bash
  # Create backup just in case
 ssh root@venus.local "mv /opt/victronenergy/gui/qml/PageSettingsRelay.qml /opt/victronenergy/gui/qml/PageSettingsRelay.qml.bak && mv /etc/venus/gpio_list  /etc/venus/gpio_list.bak"
 # Edit gpio_list file according to your needs BEFORE you copy it
 scp gpio_list root@venus.local:/etc/venus/gpio_list
 # Adjust gui file
 scp PageSettingsRelayAdditionalManualSwitches.qml root@venus.local:/opt/victronenergy/gui/qml/PageSettingsRelay.qml
 # Reboot venus os
 ssh root@venus.local "reboot"
 ```
 ## Hardware
 This was tested using this [4 relay board](https://www.az-delivery.de/en/products/4-relais-modul?variant=40226959442&utm_source=google&utm_medium=cpc&utm_campaign=azd_de_google_performance-max_labelled-products&utm_content=&utm_term=&gclid=CjwKCAjwkMeUBhBuEiwA4hpqECBu5CbRelAK9IeToxeLzvigR0BHciozznbtJA3JMiaMwAQvA_LBhxoCy78QAvD_BwE) Connected to GPIO 17,18,27,22 as seen in the [gpio_list](./gpio_list) file. You can use every free GPIO pin. If you use another relay board make sure that the io on your board is for 3.3v logic level.   
