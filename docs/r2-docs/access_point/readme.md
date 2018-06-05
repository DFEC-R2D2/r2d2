---
title: Roomba's WiFi Access
author: Kevin J. Walchko
header-includes:
    - \usepackage{fancyhdr}
    - \pagestyle{fancy}
    - \fancyhead[CO,CE]{ECE 387}
    - \fancyfoot[CO,CE]{\thepage}
    - \fancyfoot[LE,RO]{Robots are cool!}
abstract: This will show you how to setup direct wifi access to the Roomba without having to worry about getting out of range of the D-Link access point.
---

# Roomba

Use [mote](https://github.com/MomsFriendlyRobotCompany/mote) for the initial setup. Then follow the instructions
here for more.

**NOTE:** Because of various security issues (I can't buy thumb drives ... really?),
this had to be changed to username t5/t6 and I am now using only the built in
wifi, no USB wifi dongle. If you see it still in this guide (or else where), then
I just missed removing the old info.

**NOTE:** The `pi` user account has the password changed, so students cannot log
into it. The student user accounts will be either `t5` or `t6` (yes, real original,
but I honestly don't think they will remember those) with the password `raspberry`.
There are so many moving parts with this new course, I don't want to have to track
password too. You could do this in the future to ensure a group isn't looking at
another group's code and cheating.

## User Accounts

Usernames and passwords (including SMB access) are:

- `t5`: raspberry
- `t6`: raspberry
- `pi`: I changed it from the default so students don't know it

If you need to [reset a password](https://www.computerhope.com/unix/upasswor.htm):

  passwd <username>

# Wifi and Access Point Setup

Setting up the RPi as an [access point](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md#internet-sharing) so you can log directly into it without needing an access
point. We always had issues of the robots getting out of range of the base station,
this will solve that problem, because you can simply follow the robot around with
a laptop, iPad, or whatever logged in.

We are going to use the built in wifi (wlan0) on the RPi 3 to host a local
dhcp server.

1. Install packages:

		sudo apt-get install dnsmasq hostapd
		sudo systemctl stop dnsmasq
		sudo systemctl stop hostapd

1. Now add `denyinterfaces wlan0` to `/etc/dhcpcd.conf` so we don't self assign ip
   addresses to ourself on `wlan0`. However, it is okay if another dhcp server gives
   `eth0` (the wired network interface) an ip address

1. Edit `/etc/network/interfaces` so our `wlan1` interface has a static ip address:

		allow-hotplug wlan0  
		iface wlan0 inet static  
		    address 10.10.10.1
		    netmask 255.255.255.0
		    network 10.10.10.0

1. Setup dnsmasq

		sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
		sudo nano /etc/dnsmasq.conf

   Then add the following lines which say which interface to use and min ip address, max ip address, mask, and how long it is valid for:

   	interface=wlan0      # Use the usb wifi dongle
		dhcp-range=10.10.10.5,10.10.10.100,255.255.255.0,24h

1. Setup hostapd config file: `/etc/hostapd/hostapd.conf`, note, we are setting
up the SSID name the same as the hostname:

		interface=wlan0
		ssid=<NameOfNetwork>
		channel=10
		auth_algs=1
		wpa=2
		wpa_passphrase=<password_atleast_8_characters>
		wpa_key_mgmt=WPA-PSK
		wpa_pairwise=CCMP
		rsn_pairwise=CCMP

1. Remove `/etc/init.d/hostapd` since it is unnecessary

1. Create `/etc/system.d/system/hostapd.service`:
    ```bash
    [Unit]
		Description=Hostapd Access Point
		After=sys-subsystem-net-devices-wlan0.device
		BindsTo=sys-subsystem-net-devices-wlan0.device

		[Service]
		Type=forking
		PIDFile=/var/run/hostapd.pid
		ExecStart=/usr/sbin/hostapd -B /etc/hostapd/hostapd.conf -P /var/run/hostapd.pid

		[Install]
		WantedBy=multi-user.target
    ```
	*Note:* if you are using an interface other than wlan0, make the correct
	change above.

1. Now do:

		sudo systemctl enable hostapd
		sudo systemctl start hostapd

1. Finally, double check all is well with `service hostapd status` which should show
  everything is up and running.

There should be a script `setup-access-point.sh` that will automate this for you.

# Login

Now you should be able to join your robot's wifi using the SSID and WPA passphrase.
Then login via `ssh`:

	ssh <username>@<robot_name>.local
	ssh <username>@10.10.10.1
