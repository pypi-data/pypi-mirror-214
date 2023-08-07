# About
This is a simple script to automatically switch between network interfaces on a Linux system when a remote host is unreachable, as tested with ping or curl.

When the primary interface is not working, a secondary interface will be used. When the primary interface is working again, the system will automatically swap back to it. If none of the interfaces are working, the script will reboot the system after a given amount of retries.

# Installation

Use `./install.sh` to install. It:

1. Runs `pip3 install network-fallback-service` to install the two executables in your path: `network-fallback-launch` and `network-fallback-config`

2. Runs the interactive config utility `network-fallback-config` to create a new config for your device. Also creates the `systemd` service file in `/etc/systemd/system/network-fallback.service` and reloads the systemd daemon

# Usage

Use systemctl to start/stop the service:

`systemctl enable --now network-fallback.service`

`systemctl disable --now network-fallback.service`

## Defining interfaces
To ensure an interface is compatible with this service, it should be set up in ifupdown or NetworkManager, two of the common Linux network interface managers. Your config should be detailed enough that NetworkManager can enable the interface simply running `nmcli dev connect <interface>`. Refer to the NetworkManager documentation for more information.

### Ethernet
`eth0` should work with no extra config (considering the IP settings are correct for your install site. Static IP / DHCP setting can be adjusted in `ai-config`)

### WiFi
`wlan0` will work given you have created a wireless network connection before. See `nmcli` documentation for adding to a wifi network. It will likely be like this:

1. `nmcli radio wifi on` to make sure its on

2. `nmcli dev wifi list` to see list of SSIDs

3. `sudo nmcli dev wifi connect <SSID> password "<Passowrd>"`

### Other Interfaces

All NetworkManager interfaces must be configured so that NetworkManager knows how to adjust the routing table properly when running `nmcli dev connect <interface>`. Check the NetworkManager documentation for more information on setting up your specific use case.

## Manual Config
The config files are located in `/etc/network-fallback.d`, with the following format:
```
[iface.NAME]
primary = true
type = ifupdown
persistent = true

[iface.NAME]
type = NetworkManager
gateway = 192.168.0.1
persistent = true

[check.ping]
type = ping
host = 8.8.8.8
makeRoute = true

[checks]
interval = 30
retryLimit = 6

[system]
debugLogs = true/false
```
`[iface.NAME]`

- Supply the interface name in the section header

- `primary`, for if this is the primary interface

- `gateway`, for if this interface accesses the internet via a gateway (ie a router)

- `persistent`, controls if the device should be disabled if it keeps failing (more than 5 times in a row)

`[checks.NAME]`

- Name of the check can be anything unique

- `type`, may be ping or curl, this is how to test connection to the host

- `host`, is the ip address to test connection to

- `makeRoute`, is if a temporary route to this host should be added to perform this connection check (useful for when the gateway must be defined to reach host on a given interface, ie an ethernet network with a router)

`[checks]`

- `interval`, time in seconds between checks.

- `retryLimit`, how many failed checks in a row can be tolerated before rebooting.

`[system]`

- `debugLogs` enables verbose output to stdout. Note stdout/stderr is captured by the systemd journal if running as a service.

## Viewing Logs

All logs can be viewed with `journalctl -u network-fallback`, and the service status with `systemctl status network-fallback.service`.