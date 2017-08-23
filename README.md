# Wifi Test
wifi test sequence

This module uses iperf package for Linux distributions. The python script establishes a test sequence and logs the results.
edit /etc/udev/rules.d/70-persistent-net.rules for wlan* config

Requirements:

* iperf server (either with another computer or router running Openwrt)
* iperf2 or iperf3 package for Linux distribution (similar command lines)
* argparse for python (should be included in most python releases, otherwise copy argparse.py to system path)

usage: main.py [-h] [-a [ADDRESS]] [-i [INTERFACE]] [-w [WINDOW]] [-n [BUFFER]] [-c [CYCLE]]

optional arguments:

-h, --help show this help message and exit

-a [ADDRESS] IP address or name of server

-i [INTERFACE] wlan interface (default: wlan0)

-w [WINDOW] TCP window size

-n [BUFFER] Transfer file size

-c [CYCLE] number of cycles
