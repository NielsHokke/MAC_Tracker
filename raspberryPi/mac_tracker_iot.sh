#!/bin/bash

echo 'Synchronizing date and  time'

ntpdate ntp0.nl.net

echo 'starting webcam loop'  

python webcam.py &

echo 'setting wlan0 to monitoring mode'

airmon-ng check kill
mon0up

echo 'enable channel hopping'

./chanhop.sh -i mon0 &

sleep 1

echo 'start sniffing'

tshark -n -t ad -b duration:300 -i mon0  -T fields -e frame.time_epoch -e wlan.sa -e wlan.da -e wlan.fc.type_subtype -e wlan_radio.signal_dbm -w data 'not subtype beacon' >> ./output.csv 

