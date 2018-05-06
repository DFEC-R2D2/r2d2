
<img src="pics/header.jpg" width="100%">

[![Build Status](https://travis-ci.org/DFEC-R2D2/r2d2.svg?branch=master)](https://travis-ci.org/DFEC-R2D2/r2d2)

# R2-D2 Senior Design Project

This repo documents the progress of the R2-D2 design for the 2017-2018 class year. R2-D2's purpose, once
it is delivered, is to:

- Serve as an example of multi-diciplinary engineering
- Support internal events like: Major's Night, DF evnets, and DFEC events
- Support external events like: STEM outreach and recruiting events.

# Architecture

## Power

The power system is modeled around a common 12V system. Relays are used to route power for emergency stop, charging, or other reasons.

![](pics/design/R2-D2-Power-v2.png)

Although there are mulitple batteries, they are all the same type of battery and therefore take the
same type of charging. The battery chemestry and capacity is TBD.

## Data

The system data shows the wiring between the pi and all of the sensors and effectors. Most of the communications operates at 3.3v, however, there is a USB serial that operates at 5v (5V TTL). The pi uses all of the buses available to it: I2C at 100 Hz, SPI, and USB. The PWM to drive the servos is off loaded to a hardware servo controller board. Similarly, the PWM which drives the motors is offloaded to 2 different motor controllers (Sabertooth and SMC).

![](pics/design/r2d2-data.png)

## Software Operating Modes

![](pics/design/r2d2_states.png)

The system shall follow the transition diagram shown above with the following definitions:

- **Off:** No R2D2 software is running and the Raspberry Pi (RPi) may or may not be powered on. This is
  not so much a designed software state so much as a reality of "off".
- **Standby:** When R2 software is started, it will enter this state and remain until commanded to exit.
  No motor (servos, legs, or dome) are allowed to run. This state produces and is capable of recording
  telemetry. This state is the only state where charging will occur. When the power plug is connected,
  the robot will change from whatever state it is in to this one.
- **Remote Controlled:** When commanded into this state, the robot will except commands from the
  joystick. The commands will be followed except where sensor (TBD) detect hazards and prevent the
  operator from damaging the robot. In this state, all motors are enabled.
- **Display:** When commanded into this state, the robot acts like a robotic static display. The leg
  motors are not enabled, however the dome motor is able to move. This mode is entered either by
  a software command or external power supplied to the robot which will trigger relays and automatically
  cut power to the leg motors.
- **Autonomous [objective]:** When commanded into this mode, the robot will autonomous move and avoid obstacles
  using its onboard sensors (TBD). When any issue arrises (i.e., motor currents exceeded, loss of
  sensors prohibiting safe opperation, TBD) the robot will immediately go to standby mode.

The system shall be designed to run the R2 software as a Debian service under `systemd`
once everything works. During development, this won't be implemented for safety reasons.

# Statement of Work

[SOW](docs/design_2017-2018/R2D2-2017.pdf)

# Software

R2 is written primarily in python. The following libraries were developed for R2-D2:

- [Text-to-Astromech: ttastromech](https://pypi.python.org/pypi/ttastromech)
- [Simple Motor Controler: smc](https://pypi.python.org/pypi/smc)
- [Sabertooth Motor Controller: pysabertooth](https://pypi.python.org/pypi/pysabertooth)

The following are used:

- [mote](https://github.com/MomsFriendlyRobotCompany/mote)
- [fake_rpi](https://pypi.python.org/pypi/fake-rpi)
- [opencvutils](https://pypi.python.org/pypi/opencvutils)
- [nxp_imu](https://pypi.python.org/pypi/nxp-imu)
- [mcp3208](https://pypi.python.org/pypi/mcp3208)

The following was created for the purpose of R2D2's code simplicity, which combines the above codes into one python library file:

- [library]

The R2D2 code can be found in the directory called Final with the python file named run.py. Currently, the Raspberry Pi 3 image that we created allows R2D2 to automatically run this code when booted on. All the USB devices that are connected to the R2D2 are based on our actual model, and would need to be changed to match the serial information of the new device if you are considering making another R2D2.
