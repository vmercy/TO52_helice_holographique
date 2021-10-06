#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
addressable_strip/main.py: Draft script aiming to test an addressable LED strip with following reference: sj-100144-102
"""
from apa102_pi.driver import apa102
from time import sleep

strip = apa102.APA102(num_led=144, order='rgb')

strip.clear_strip()

nbLeds = 144//3

for i in range(0,nbLeds):
  strip.set_pixel_rgb(i,  0x0000FF)
for i in range(nbLeds,2*nbLeds):
  strip.set_pixel_rgb(i,  0xFFFFFF)
for i in range(2*nbLeds,3*nbLeds):
  strip.set_pixel_rgb(i,  0xFF0000)

strip.show()

sleep(10)

strip.cleanup()