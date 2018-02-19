# MAC_Tracker

Project for tracking MAC-address using an ESP-32 or raspberryPi and wireshark

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

#### ESP-32

* DOIT ESP32 DEVKIT [ebay link](https://www.ebay.com/itm/DOIT-Development-Board-WiFi-Bluetooth-Low-Consumption-Dual-Core-ESP-32-ESP-2018/173061599471?epid=843519115&hash=item284b4670ef:g:BxIAAOSww9xZC~gr)
* follow [this](http://dagrende.blogspot.nl/2017/01/how-to-use-doit-esp32-devkit.html) to get started with DOIT ESP32 DEVKIT
* install [ArduinoPcap](https://github.com/spacehuhn/ArduinoPcap) libary from [spacehuhn](https://github.com/spacehuhn)

#### raspberryPi

* raspberry Pi with wifi. Can be raspberryPi3/RaspberryPi Zero W or older Pi with wifi-dongle which supports monitor mode
* [kali](https://docs.kali.org/kali-on-arm/install-kali-linux-arm-raspberry-pi) or other OS for the pi
* If not already in OS [wireshark](https://askubuntu.com/questions/700712/how-to-install-wireshark)
* tshark
```
sudo apt-get update
sudo apt-get install tshark
```

### Installing

#### ESP-32
* Follow [this guide](https://github.com/espressif/arduino-esp32/tree/master/libraries/SD) to connect SD-card to the DOIT ESP32 DEVKIT
* Install code from arduino folder to the ESP-32

#### raspberryPi

* Install [kali](https://docs.kali.org/kali-on-arm/install-kali-linux-arm-raspberry-pi) or other OS on the pi
* Install tshark by running:
```
sudo apt-get update
sudo apt-get install tshark
```
* Download MAC_Tracker.py to pi
* Adjust settings by changing
```
interface = "wlan0"
duration = 300
file_prefix = "data"
capture_filter = "not subtype beacon"
output_dir = "output"
```

* run python file
```
cd /place/of/MAC_Tracker.py
sudo pyhton MAC_Tracker.py
```

## Authors

* **Niels Hokke** - *Initial work* - [NielsHokke](https://github.com/NielsHokke)
* **Jetse Brouwer** - *Initial work* - [JetseBrouwer](https://github.com/JetseBrouwer)


## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
