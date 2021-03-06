#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
addressable_strip/main.py: Draft script aiming to test an addressable LED strip with following reference: sj-100144-102
Tutorial: https://pimylifeup.com/raspberry-pi-led-strip-apa102/
Wiring:
Strip #1 (SPI0)
| Raspberry Pi (physical) 	| APA102 LED Strip 	|
|-------------------------	|------------------	|
| /                       	| red              	|
| 6 (GND)                 	| black            	|
| 23 (SCLK)               	| yellow            |
| 19 (MOSI)               	| green           	|
Strip #2 (SPI1)
| Raspberry Pi (physical) 	| APA102 LED Strip 	|
|-------------------------	|------------------	|
| /                       	| red              	|
| 6 (GND)                 	| black            	|
| 40 (SCLK1 = GPIO 21)     	| yellow            |
| 38 (MOSI1 = GPIO 20)     	| green           	|
"""
from apa102_pi.driver import apa102
from time import sleep, time
import signal
import sys

strip = apa102.APA102(num_led=144, order='rgb')
strip2 = apa102.APA102(num_led=144, order='rgb', mosi=20, sclk=21)

""" def signal_handler(sig, frame):
    global strip
    print('Extinction du bandeau')
    strip.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler) """

strip.clear_strip()

nbLeds = 50
for i in range(nbLeds):
  strip.set_pixel_rgb(i,  0xFF0000 if i%2 else 0x0000FF)
for i in range(nbLeds):
  strip2.set_pixel_rgb(i, 0x0000FF if i%2 else 0xFF0000)

for i in range(60):
  strip.show()
  strip2.show()
  sleep(1)
strip.cleanup()
strip2.cleanup()