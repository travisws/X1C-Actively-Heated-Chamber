## README.md

# X1C Actively Heated Chamber

## Description

The X1C Actively Heated Chamber utilizes a Raspberry Pi Zero W to monitor and control 24v heating elements, maintaining an optimal temperature within the X1C chamber without external power sources. A web interface allows the users to set a timer aligned with the expected print completion time. Once reached, the system deactivates the heating elements, letting the print cool naturally. This is particularly beneficial for prints using ABS plastic or other high-temperature filaments. Notably, the entire system operates using the X1C's integrated power supply.

## Materials Required

To set up the X1C Actively Heated Chamber, you will need the following materials:

- Raspberry Pi Zero W (or Raspberry Pi Zero 2 W) with a Micro SD card
- Mini Mp1584EN DC-DC buck converter (24v to 5v input range)
- Noctua NF-A4x10 3-pin fan (or any equivalent 5V fan)
- 24v heating elements (flat type, 30w or less)
- AHT20+BMP280 sensors (chosen based on availability)
- Standard soldering equipment
- Assorted wires and connectors (Dupont connectors recommended)

## Installation

To install and configure the X1C Actively Heated Chamber, follow these steps:

1. Install the Raspberry Pi OS onto the SD card and pre-configure it for headless Wi-Fi connectivity.
2. Insert the SD card into the Raspberry Pi and power it on.
3. SSH into the system and configure a static IP either through your router or directly on the system.
4. Update the root password.
5. Modify the `/etc/ssh/sshd_config` file to enable root SSH login and permit password authentication.
6. Ensure Ansible is installed on your PC or server.
7. Navigate to the project's directory that you've downloaded.
8. Execute the Ansible playbook `godspeed-playbook.yml`. Familiarity with Ansible is beneficial.
9. Relax, and if all processes go smoothly, the setup should conclude in approximately two hours, if not sooner.

Note: Wiring instructions are still in progress and will be provided later.

## Usage

To use the X1C Actively Heated Chamber, access the web interface by navigating to your Raspberry Pi's IP address on port 5000. This will allow you to set desired temperatures and durations while also providing real-time monitoring of chamber temperature and humidity.

## License

This project is licensed under a license that prohibits businesses from commercializing the idea. However, individual users are free to utilize the project without restrictions.