# EZ Softether

## Purpose of this software

This software is written for making starting / stopping / routing softether on Linux easier and faster.

![ezsoftether](https://user-images.githubusercontent.com/21986859/42424263-8bafa062-82d7-11e8-83da-06c2df2eddb2.png)

## Usage

### Prerequisites

You need to have softether for linux compiled and installed before using this software. You may find tutorials on Google. This software CANNOT help you install nor configure the vpn client.

### Download EZ Softether

```bash
git clone https://github.com/K4YT3X/EZ-Softether.git
```

### Run EZ Softether

```bash
sudo python3 ezsoftether.py -i [VPN Interface] -g [Gateway Address] --start / --stop
```

### Detailed Usages

```
usage: ezsoftether.py [-h] [-s] [-r] [-i INTERFACE] [-g GATEWAY] [-v]

optional arguments:
  -h, --help            show this help message and exit

Controls:
  -s, --start           Start VPN client and route traffic
  -r, --stop            Stop VPN client and restore original connection
  -i INTERFACE, --interface INTERFACE
                        Specify the vpn interface
  -g GATEWAY, --gateway GATEWAY
                        Specify remote gateway (server) address
  -v, --version         Print software version and legal information
```