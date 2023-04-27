# Automated Connect 4 Opponent: CSCE 462 Final Project

For our final project, we made an electronic Connect 4 game. The project comes in two parts: a peripheral with lights and buttons to connect to a Raspberry Pi, and a software package for running the game. The game allows for two users to play a game of Connect 4 against each other, and even more importantly, it features a single-player game mode for playing against the CPU.

This prototype and program were developed as a final project for CSCE 462: Microcomputer Systems at Texas A&M.

**Developers:**
 - Sam Prewett
 - Joshua Yan

## Hardware

To use the device, all you need is a Raspberry Pi with 40-pin GPIO. You connect the game board to the microcontroller with the provided cable, and you plug in both the microcontroller and the game board's 5V power supply.

You can test to make sure the power supply, level converter, and light matrix are working properly by calling

```sudo python test_lights.py```

## Software

The necessary files for running the program are *connect4.py*, the *images* folder, and the *solver* folder.

*connect4.py* is the main file. It handles both the gameplay and the hardware interaction.

*images* contains the images that scroll across the screen.

*solver* contains the code for the autoplayer's algorithm. It will need to be compiled before the game can be played (see **Compilation**).

### Compilation

You will need to compile the C++ files in the *solver* folder on the Raspberry Pi before the program can be run. To do this, navigate into the *solver* folder in a terminal on the Raspberry Pi and call

```g++ -std=c++17 *.cpp```

It is necessary that the compiled program have the relative path *solver/a.out*.

### Hardware Interface

You will also need to enable SPI on the microcontroller to control the light matrix. To do this, call

```sudo raspi-config```

From there, navigate to *Interfaces* and enable SPI.

### Libraries

It is necessary that the NeoPixel library be installed on the Pi. For instructions on how to install this library, please refer to https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage.

### Usage

After compilation, to start the game, simply call (from the repository's root folder)

```sudo python connect4.py```

It is necessary that Python be on version 3 or above. If need be, replace `python` in the command with `python3`.

### Run on Startup

To start the game on boot so that you do not have to SSH into the Pi or use the graphical interface, call

```sudo nano /etc/rc.local```

and add the line

```sudo python [path to repository]/connect4.py &```

Do not forget the ampersand, as this makes the program run in the background.