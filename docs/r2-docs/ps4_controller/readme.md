---
title: Setting Up PS4 Controller with Linux Raspbian
author: Kevin J. Walchko
header-includes:
    - \usepackage{fancyhdr}
    - \pagestyle{fancy}
    - \fancyhead[CO,CE]{ECE 387}
    - \fancyfoot[CO,CE]{\thepage}
    - \fancyfoot[LE,RO]{Robots are cool!}
abstract: This will show you how to setup a bluetooth PS4 controller on a Raspberry Pi with Linux Raspbian. You won't have access to *everything*, like the accels and gyros, but you will have all of the buttons and analog sticks. Then using python and SDL2, I can easily interface with joystick.
---

# PS4 Controller

![Sony PS4 Dual Shock Controller](pics/ps4.jpg){width=50%}

## Setup Bluetooth and Pairing

Log into your Raspberry Pi either via SSH or using a keyboard, at the console:

```bash
	sudo systemctl enable bluetooth.service
	sudo systemctl start bluetooth.service
```

Pairing using `bluetoothctl`:

```bash
	sudo bluetoothctl
```

Some of the commands available:

```bash
	[bluetooth]$ help
	Available commands:
	  list                       List available controllers
	  show [ctrl]                Controller information
	  select <ctrl>              Select default controller
	  devices                    List available devices
	  paired-devices             List paired devices
	  power <on/off>             Set controller power
	  pairable <on/off>          Set controller pairable mode
	  discoverable <on/off>      Set controller discoverable mode
	  agent <on/off/capability>  Enable/disable agent with given capability
	  default-agent              Set agent as the default one
	  scan <on/off>              Scan for devices
	  info <dev>                 Device information
	  pair <dev>                 Pair with device
	  trust <dev>                Trust device
	  untrust <dev>              Untrust device
	  block <dev>                Block device
	  unblock <dev>              Unblock device
	  remove <dev>               Remove device
	  connect <dev>              Connect device
	  disconnect <dev>           Disconnect device
	  version                    Display version
	  quit                       Quit program
```

At the `bluetoothctl` prompt type the following commands:

```bash
	agent on
	default-agent
	power on
	discoverable on
	pairable on
	scan on
```

Example output can be found below:

```bash
	[pi@pes ~]$ bluetoothctl
	[NEW] Controller 00:15:XX:XX:XX:XX pes [default]
	[bluetooth]# agent on
	Agent registered
	[bluetooth]# default-agent
	Default agent request successful
	[bluetooth]# power on
	Changing power on succeeded
	[bluetooth]# discoverable on
	Changing discoverable on succeeded
	[CHG] Controller 00:15:XX:XX:XX:XX Discoverable: yes
	[bluetooth]# pairable on
	Changing pairable on succeeded
	[bluetooth]# scan on
	Discovery started
```

Now put your Sony PlayStation 4 control pad into pairable mode by holding down
the Share and PlayStation buttons until the light bar on the control pad flashes
yellow. After a few seconds you should see at the `bluetoothctl` prompt that
your control pad has been discovered, e.g.:

```bash
	[bluetooth]# scan on
	Discovery started
	[CHG] Controller 00:15:XX:XX:XX:XX Discovering: yes
	[NEW] Device 00:3C:XX:XX:XX:XX 00-3C-XX-XX-XX-XX
	[NEW] Device 1C:66:XX:XX:XX:XX 1C-66-XX-XX-XX-XX
	[CHG] Device 1C:66:XX:XX:XX:XX LegacyPairing: no
	[CHG] Device 1C:66:XX:XX:XX:XX Name: Wireless Controller
	[CHG] Device 1C:66:XX:XX:XX:XX Alias: Wireless Controller
	[CHG] Device 1C:66:XX:XX:XX:XX LegacyPairing: yes
	[CHG] Device 1C:66:XX:XX:XX:XX Class: 0x002508
	[CHG] Device 1C:66:XX:XX:XX:XX Icon: input-gaming
```

Take a note of the Bluetooth MAC address shown for “Wireless Controller”, e.g.
1C:66:XX:XX:XX:XX in my case.

Now type:

```bash
	pair MAC
```

where MAC is the MAC address of your controller. If asked, enter 0000
as the PIN, for example:

```bash
	[bluetooth]# pair 1C:66:XX:XX:XX:XX
	Attempting to pair with 1C:66:XX:XX:XX:XX
	[CHG] Device 1C:66:XX:XX:XX:XX Connected: yes
	Request PIN code
	[agent] Enter PIN code: 0000
	[CHG] Device 1C:66:XX:XX:XX:XX Modalias: usb:v054Cp05C4d0100
	[CHG] Device 1C:66:XX:XX:XX:XX UUIDs: 00001124-0000-1000-8000-00805f9b34fb
	[CHG] Device 1C:66:XX:XX:XX:XX UUIDs: 00001200-0000-1000-8000-00805f9b34fb
	[CHG] Device 1C:66:XX:XX:XX:XX Paired: yes
	Pairing successful
	[CHG] Device 1C:66:XX:XX:XX:XX Connected: no
```

I believe the PIN is only required on the older PS3 controllers and not the newer
PS4 ones. Next we must trust the controller by running:

```bash
	trust MAC
```

where MAC is the MAC address of your control pad, for example:

```bash
	[bluetooth]# trust 1C:66:XX:XX:XX:XX
	[CHG] Device 1C:66:XX:XX:XX:XX Trusted: yes
	Changing 1C:66:XX:XX:XX:XX trust succeeded
```

Finally, run the following command to connect to the controller:

```bash
	[bluetooth]# connect 1C:66:XX:XX:XX:XX
	Attempting to connect to 1C:66:XX:XX:XX:XX
	[CHG] Device 1C:66:XX:XX:XX:XX Connected: yes
	Connection successful
```

Then type `quit` to exit back to the command prompt. You should now see that
the light bar on your control pad is blue.

Other useful info:

```bash
	[bluetooth]# info 1C:66:xx:xx:xx:xx
	Device 1C:66:xx:xx:xx:xx
		Name: Wireless Controller
		Alias: Wireless Controller
		Class: 0x002508
		Icon: input-gaming
		Paired: yes
		Trusted: yes
		Blocked: no
		Connected: yes
		LegacyPairing: no
		UUID: Human Interface Device... (00001124-0000-1000-8000-00805f9b34fb)
		UUID: PnP Information           (00001200-0000-1000-8000-00805f9b34fb)
		Modalias: usb:v054Cp05C4d0100


	[bluetooth]# paired-devices
	Device 1C:66:xx:xx:xx:xx Wireless Controller


	[bluetooth]# connect 1C:66:xx:xx:xx:xx
	Attempting to connect to 1C:66:xx:xx:xx:xx
	Connection successful


	[bluetooth]# disconnect 1C:66:6D:76:9B:B4
	Attempting to disconnect from 1C:66:xx:xx:xx:xx
	Successful disconnected
	[CHG] Device 1C:66:xx:xx:xx:xx Connected: no
```

## Reconnect after reboot

1. put PS4 controller into pairable mode (press PS button and Share), the front light bar will flash.
2. run `bluetoothctl`
	1. connect 1C:66:6D:76:9B:B4

# Debug

When paired, you should see strange characters appear when you use the joystick:

```bash
	cat /dev/input/js0
```

This is because you are reading the raw digital joystick info and the command line
is trying to convert that to printable characters for you. If you want something
a little more useful, you can use `jstest` from the joystick package to see
more meaningful info:

```bash
	sudo apt-get install joystick
	jstest /dev/input/js0
```

# `ds4drv`

Early on, I had to install this. It did a great job, but recent kernels and the
newer Debian Stretch (which Raspbian is based on), doesn't seem to need it.
However, it did give me access to the accelerometer and gyros, but I generally
don't need them.

So do `pip install ds4drv` (you need version 0.5.1 to work on jessie/rpi3) and
it will go through and pair your device. Also follow the instructions on
[ds4drv](https://github.com/chrippa/ds4drv) to setup udev right. Then run:

	ds4drv

This will pair and setup your joystick to work (I use SDL2 as my joystick interface)
and it work great.

Also note, the light bar in the front should be strong, bright blue when paired.

-------------------------------------------------------------------------------

# References

* [Bluetooth PS4 reference](http://pes.mundayweb.com/html/Using%20PS4%20Control%20Pads%20via%20Bluetooth.html)
* [PS4 wiki](http://www.psdevwiki.com/ps4/DualShock_4)
* http://eleccelerator.com/wiki/index.php?title=DualShock_4
* [ds4drv](https://github.com/chrippa/ds4drv)
