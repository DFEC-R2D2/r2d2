
<img src="pics/header.jpg" width="100%">

[![Build Status](https://travis-ci.org/DFEC-R2D2/r2d2.svg?branch=master)](https://travis-ci.org/DFEC-R2D2/r2d2)

# R2-D2 Senior Design Project

This repo documents the progress of the R2-D2 design for the 2017-2018 class year.

## Architecture

### Power

![](pics/design/R2-D2-Power.png)

### Data

![](pics/design/r2d2-data.png)

### Software

![](pics/design/r2d2-sw.png)

## Requirements

1. R2 shall operate in one of three modes:
    
	    a. *remote controlled* [threshold] - R2 shall allow semi-autonomous operation (via a bluetooth joystick) where the user can drive R2 anywhere. However, R2 will also use all onboard sensors to help ensure (to the best of its ability) the user doesn't damage R2 or issues an unsafe command.
		b. *static display* [threshold] - R2 shall remain stationary (power cut to leg motors) and shall interact with people passing by. Dome motor and servo motors in dome shall continue to have power and operate
		c. *autonomous* [objective] - R2 shall navigate Fairchild hallways without bumping into any person or object
		d. *standby* [threshold] - This is the default boot up mode and charging mode for R2. In this mode, not motion commands are excepted. Under the following situations, R2 will automatically switch to this mode:
		
			    1. charging: R2 shall switch to standby and remain in standby until charging power is disconnected
				2.  ... maybe a diagram in stead???
				

2. When the emergency stop (EMS) button is pressed, R2 shall stop with no power going to all motors, but all electronics shall continue to operate. The EMS shall be mounted where R2's inhibitor switch is located in Episode IV.

3. R2's sensor suite shall allow:

        a. Measure voltage and current at the leg motor batteries and electronics battery. When batteries are low, notify user and when a prescribed depth of discharge is reached, switch operating mode to standby until batteries are charged.
		b. Sense orientation and switch to standby if R2 has fallen down (exceeds a pitch or roll in excess of a predefined value)
		c. Sense Earth's magnetic field, process the information, and use for navigation as needed
		d. Sense angle of dome in order to point the dome in a defined direction
		e. [objective] Sense loud noises and determine the direction
		f. [objective] Record audio for speech-to-text processing
		g. Capture video for on-board processing as needed and streaming (mjpeg) to any standards compliant browser
		h. [objective] Measure leg wheel rotations and process data to determine distance travelled (odometry)
		i. [objective] R2 shall sense stairs and drop-offs (or absence of floor) 360 degress around it along the floor plane
		j. [objective] R2 shall sense obstacles 360 degrees around it along the floor plane
		k.

4. R2's interior shall be clean and designed to be presentation ready.

       a. All cables will will be routed and neat.
       b. All electronics shall be neatly mounted
       c. All cable shall have connectors for easy disconnecting
       d. Design shall be modular and any interior component shall be removable for maintenance without having to cut, unglue, de-solder, or damage the robot in any way.

5. R2 shall be returned to its proper appearance (as seen in Episode IV) with certain exceptions (e.g., emergency stop button):

       a. Holes in dome need to be filled in
       b. Body needs to be re-assembled and outer structure (re)painted as necessary
       c. Leg motors need to be hidden in the battery box
       d. Front leg needs to be attached
       e. Skirt needs to be attached
       f. Leg covers/decorations need to be attached
       g. Leg and dome motors need to be properly mounted

6. R2 shall be fully documented:

       a. All datasheets
       b. All trades
       c. All mechanical drawings produced
       d. All budges: power and weight
       e. All code (both commented and saved in the git repository)
