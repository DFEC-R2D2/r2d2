# R2-D2 Team Roles

## System Engineering

Responsibilities

- Owns all hardware/software diagrams
- Owns all mechanical/electrical/software interfaces
- Owns BOM and power/weight budgets
- Owns operator's manual
- Owns risk and configuration management of hardware/software/electrical
- Ensure continuous integration for software and individual engineers are documenting as go along

## Electrical Engineer

Responsibilities

- Owns mechanical chassis
- Owns power subsystem
- Owns safety shutdown
- Owns individual project (TBD)

## Computer Engineer

Responsibilities

- Owns software architecture
- Owns sensors/software drivers
- Owns raspberry pi/arduinos and software on them
- Write unit tests for everything
- Owns individual project (TBD)

# Fix Last Year's Design

| Key |                     |
|-----|---------------------|
|EE   | Electrical Engineer |
|CE   | Computer Engineer   |
|SE   | Systems Engineer    |

- [EE] Front leg needs to be correct length so R2 don't fall over so easily
- [EE] Fix charging system
    - What automatic charging system instead of manual
    - Investigate switch to NiMH
    - Investigate 383 robot chargers
    - One simple cable from a standard wall mount (or charger if not possible) 
- [CE] Modernize software
- [SE] Document system

# Topics for This Year

- Creat a decent Human/Machine interface
    - [CE] Can't tell what is working and what isn't
        - Fill in all of the LED lights R2 should have
    - [CE/EE] Need debugging tools (hardware/software) before starting individual projects
        - [CE] Webserver status
    - [CE] Run wireless joystick directly from R2
- Design R2 to be a display in the front office
    - [EE] Must be able to disable movement (external switch)
    - [EE] Must run off standard 120V wall socket
    - [CE] Must be animated and friendly
        - Notice when people enter the room
        - In some cases great people
        - In some cases recognize people (maybe too difficult)
        - Head must move (or track) people
