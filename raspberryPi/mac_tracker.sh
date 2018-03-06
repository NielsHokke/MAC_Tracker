#!/bin/bash

echo 'Synchronizing date and  time'

ntpdate ntp0.nl.net

echo 'making output dir and mounting usb'  

umount /dev/sda1
mkdir output
mount /dev/sda1 output/

echo 'setting wlan0 to monitoring mode'

airmon-ng check kill
airmon-ng start wlan0

echo 'enable channel hopping'

./chanhop.sh -i wlan0mon &

sleep 1

echo 'start sniffing'

tshark -n -t ad -b duration:300 -T fields -e frame.time_epoch -e wlan.sa -e wlan_radio.signal_dbm -w data 'subtype probereq' >> output/output.csv 

