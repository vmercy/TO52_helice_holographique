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
| 21 (SCLK)               	| yellow            |
| 20 (MOSI)               	| green           	|
"""
from apa102_pi.driver import apa102
from time import sleep
import signal
import sys

strip = apa102.APA102(num_led=144, order='rgb', mosi=19, sclk=23)

""" def signal_handler(sig, frame):
    global strip
    print('Extinction du bandeau')
    strip.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler) """

strip.clear_strip()

nbLeds = 144
freq = int(sys.argv[1])
duree = 10
delay = (1/freq)/2
while(duree>=0):
  for i in range(nbLeds):
    strip.set_pixel_rgb(i,  0xFFFFFF)
  strip.show()
  for i in range(nbLeds):
    strip.set_pixel_rgb(i,  0x000000)
  strip.show()
  duree-=2*delay

strip.cleanup()