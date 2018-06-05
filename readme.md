
<img src="pics/header.jpg" width="100%">


# R2-D2 Senior Design Project

This repo documents the progress of the R2-D2 design for the 2017-2018 class year. R2-D2's purpose, once
it is delivered, is to:

- Serve as an example of multi-disciplinary engineering
- Support internal events like: Major's Night, DF events, and DFEC events
- Support external events like: STEM outreach and recruiting events.

# Team

- C1C Anthony Talosaga: power system and software
- C1C Hwi Tae Kim: software
- C1C Brayden Thomas: mechanical design and overall build
- C1C Mario Bracamonte: mechanical design and electrical PCD design/construction

# Architecture

## Power

The power system is modeled around a common 12V system. Relays are used to route power for emergency stop, charging, or other reasons. The 12V is split into 5V and 3.3V using voltage regulators to power the raspberry pi, Arduino, pololu motor driver, LED matrix, servos, fan, and the sabertooth motor driver.

![](pics/PowerSystem.jpg)

The type of battery that we used for R2D2 is the Motorcycle Battery called Battery Tender Lithium Battery from Deltran. This battery is made from Lithium Iron Phosphate and supplies 12V with 26-35 Amps of power. This allows us to power all the components in R2D2 as well as providing power to the motors, which take up majority of the current.

## Data

The system data shows the wiring between the pi and all of the sensors and effectors. Most of the communications operates at 3.3v, however, there is a USB serial that operates at 5v (5V TTL). The pi uses all of the buses available to it: I2C at 100 Hz, SPI, and USB. The PWM to drive the servos is off loaded to a hardware servo controller board. Similarly, the PWM which drives the motors is offloaded to 2 different motor controllers (Sabertooth and SMC).

![](pics/ControlsSystem.jpg)

## Software Operating Modes

![](pics/SoftwareFlowChart.jpg)

The system shall follow the transition diagram shown above with the following definitions:

- **Off:** The off mode of R2D2 is when R2D2 is powered off or without any power source. This means that none of the operations are possible, and R2D2 non-functional.
- **Standby:** The standby mode of R2D2 is when R2D2 is remaining idle. None of the motors or the sensors are working in this mode. The Standby mode operates to allow users the ability to fix problems. It is the default mode upon turning R2D2 on.
- **Remote Controlled:** The remote mode of R2D2 can be controlled through the PS4 controller. The instructions on how to connect the PS4 controller to R2D2 can be found in the operational manual. All functionalities of R2D2 is present in this mode.
- **Static Display:** The display mode of R2D2 is used to showcase R2D2. This means that R2D2 is not capable of moving, because it is in display mode. The display mode will respond to people that are close to R2D2.


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

Folder structure

```bash
r2d2
|- final_design
   |- arduino
   |- mechanical
   |- node
   |   |-nodejs
   |     |- scripts
   |     |- movies
   |     |- pics
   |- python
      |- clips
      |- library
      |- states
```

- `arduino`: contains the Arduino code. The Arduino talks to the ultrasound sensors and measures the battery voltage
- `mechanical`: containes STL files of parts designed for R2
- `node`: R2's webpage is programmed using nodejs. The `script` folder contains 2 scripts to: 
    - `build_webpages.sh`: generate the webpage html files from Markdown and installs them in the correct location.
    - `gen_qr_code.py`: generate a QR code to enable people to easily access R2's webpage.
- `python`: this is the main *robot* code for R2. The main program is `run.py`.
    - `clips.json`: is a list of available Star Wars sound clips R2 can play

Currently, the Raspberry Pi 3 image that we created allows R2D2 to automatically run this code when booted on. All the USB devices that are connected to the R2D2 are based on our actual model, and would need to be changed to match the serial information of the new device if you are considering making another R2D2. If needed, the image file can be acquired through the DFEC Department Instructor Major Kevin Walchko.

R2 has 3 primary states:

- **standby():** This function is the standby mode function and the default state of R2. Standby does nothing but *standby* for something to happen. If there is an error during operation, R2 switches from his current operating mode and falls into standby. Since standby does nothing, it is seen as the safest mode.
- **static():** This function is the static mode. Static mode is the display mode and it is designed not to allow the leg motors to move. Infact, the electrical design flips a relay and cuts off leg motor power in this state. Only the dome motor and the servos are allowed to move in this state.
- **remote():** This function is the remote mode function, it receives the `remoteflag`, which is set by the keypad on R2D2. This flag is set when 3 is pressed, and continues to be set until R2D2 is put into another mode. The remote mode ensure that R2D2 has full capabilities, such that the motor control works, and all its functionalities are present. R2D2 will be controlled through the PS4 controller. The instructions for connecting the PS4 controller to R2D2 can be found in the operations manual.

| State   | Dome Motor | Leg Motors | Audio | Camera | LEDS/Lights | Servos |
|---------|------------|------------|-------|--------|-------------|--------|
| Standby |            |            |   X   |        |     X       |        |  
| Remote  |    X       |     X      |   X   |        |     X       |    X   | 
| Static  |    X       |            |   X   |   X    |     X       |    X   | 

Helper functions:

- **reboot():** This function is the reboot function. 
- **shutdown():** This function is the shutdown function. 

R2 has to have some personnality, so he is setup with these *emotions*:

- **happy():** This function does not have any inputs or outputs, as the commands are given from the function. The happy function turns on the green LED on the 8x8 matrix LED pads, and also spins the dome. The top hatch of R2D2 will open in a wave and close in a wave. This can be either called from the keypad button 4, or from the arrow hat on the controller.
- **confused():** This function does not have any inputs or outputs, as the commands are given from the function. The happy function turns on the orange LED on the 8x8 matrix LED pads. This can be either called from the keypad button 5, or from the arrow hat on the controller.
- **angry():** This function does not have any inputs or outputs, as the commands are given from the function. The happy function turns on the red LED on the 8x8 matrix LED pads, and plays the imperial theme sound. Once the theme sound is complete, it opens the top hatch of R2D2 and closes it afterwards. This can be either called from the keypad button 6, or from the arrow hat on the controller.


# Project in Pictures

The development of R2 followed a standard Aerospace process of building/testing a breadboard, brassboard, and final design. These follow the ideas of form, fit, and function.

- **Breadboard**: This was the first incarnation of R2. As seen below, it consisted of HW/SW that allowed the team to design/test the functional aspects of R2. The breadboard contained either the actual HW R2 would use or surrogate hardware that was in some way representative (as best as we knew it at the time of the build) of the final design.
- **Brassboard**: This was the second incarnation of R2. Building upon the breadboard HW/SW, all surrogate items were swapped out for the correct items. For example, the breadboard had 3 small 12V motors which represented the dome and leg motors. Now in the brassboard, these small motors were replaced with the final R2 motors. The brassboard now allowed us to test both function and fit. Fit refers to the interfaces, both HW and SW. 
- **Final Design**: Usually you would go to a prototype in the Aerospace world, but here we went straight to the final design. This final design now allowed us to test HW/SW form, fit, and function.  Form refers to either the physical dimension (e.g., the size of a box) or a SW size/processing standpoint for our storage system/CPU.

## Functional Development: Breadboard

This was R2's electronics on a box. It allowed full software design/testing with similar hardware without worrying about actually having R2's body built. Although this looks nothing like an R2 unit, it allowed the team to develop a decent first version of R2. Basic functionallity was achieved including:

- Face detection using OpenCV and the PiCamera
- PS4 controller integration, with analog sticks driving motors, buttons moving servos and making R2 sounds

<img src="pics/bread-board-1.jpg" height="400px">

<img src="pics/bread-board-2.jpg" height="400px">

<img src="pics/bread-board-3.jpg" width="400px">

<img src="pics/bread-board-4.jpg" width="400px">

<img src="pics/bread-board-5.jpg" width="400px">

# Fit Development: Brassboard

This was the next level and allowed development/testing against the exact hardware and interfaces in R2. This allowed the team setup the full wiring harness with relays, test out PCBs designed (there were several versions), test out the dome slip ring wiring harness and ensure full HW and SW integration.

<img src="pics/brass-board-1.jpg" width="400px">

<img src="pics/brass-board-2.jpg" width="400px">

<img src="pics/brass-board-3.jpg" width="400px">

<img src="pics/brass-board-4.jpg" width="400px">

<img src="pics/brass-board-5.jpg" width="400px">

<img src="pics/brass-board-6.jpg" width="400px">

# Final Design and Building

Everything from the brassboard was duplicated and built into the R2. The brassboard was **not** dismantled, but left intact for debugging. The team needed a setup that we could fall back on if HW/SW problems were encountered in the final build. 

Many of the hindges, mounting brackets, etc were designed and 3d printed. The largest design was the 2 rear feet. They were completely designed and 3d printed. Then the motors, wheels, etc were mounted inside and they were painted using Rust-Oleum paint and primer. Unfortunately there were numerous little errors that weren't discovered until everyting was assembled and we had to redesign and rebuild the feet. The feet also took about 2-3 days to print just one ... it was a very slow process.

<img src="pics/3d-print-1.jpg" width="400px">

<img src="pics/3d-print-2.jpg" width="400px">

<img src="pics/3d-print-3.jpg" width="400px">

<img src="pics/3d-print-6.jpg" width="400px">

<img src="pics/3d-print-7.jpg" width="400px">

<img src="pics/3d-print-8.jpg" width="400px">

# Integration

## Electronics

All of the electronics in the body were mounted on a clear piece of plexiglass.

<img src="pics/electronics-1.jpg" width="400px">

<img src="pics/electronics-2.jpg" width="400px">

## Dome

Mounts for all of the parts were 3d printed and epoxied to the dome. Then the electronics were bolted to the mounts.

<img src="pics/dome-1.jpg" width="400px">

<img src="pics/dome-2.jpg" width="400px">

<img src="pics/dome-3.jpg" width="400px">

<img src="pics/dome-4.jpg" width="400px">

## Everything Else

<img src="pics/dev-1.jpg" width="400px">

<img src="pics/dev-2.jpg" width="400px">

<img src="pics/dev-3.jpg" width="400px">

<img src="pics/dev-4.jpg" width="400px">

<img src="pics/dev-5.jpg" width="400px">

<img src="pics/dev-6.jpg" width="400px">

<img src="pics/dev-7.jpg" width="400px">

<img src="pics/dev-8.jpg" width="400px">

<img src="pics/dev-9.jpg" width="400px">

<img src="pics/dev-10.jpg" width="400px">

<img src="pics/dev-11.jpg" width="400px">

<img src="pics/dev-12.jpg" width="400px">

<img src="pics/dev-13.jpg" width="400px">

<img src="pics/dev-14.jpg" width="400px">

<img src="pics/dev-15.jpg" width="400px">

<img src="pics/dev-16.jpg" width="400px">

<img src="pics/dev-17.jpg" width="400px">

<img src="pics/dev-18.jpg" width="400px">

<img src="pics/dev-19.jpg" width="400px">

<img src="pics/dev-20.jpg" width="400px">

<img src="pics/dev-21.jpg" width="400px">
