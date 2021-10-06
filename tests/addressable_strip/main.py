#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
addressable_strip/main.py: Draft script aiming to test an addressable LED strip with following reference: sj-100144-102
"""
from apa102_pi.driver import apa102
from time import sleep

strip = apa102.APA102(num_led=144, order='rgb')

strip.clear_strip()

strip.set_pixel_rgb(0,  0xFF0000)  # Red
strip.set_pixel_rgb(1, 0x00FF00)  # Green
strip.set_pixel_rgb(2, 0x00FF00)  # Green
strip.set_pixel_rgb(3, 0x0000FF)  # Blue
strip.set_pixel_rgb(4, 0x0000FF)  # Blue
strip.set_pixel_rgb(5, 0x0000FF)  # Blue

strip.show()

sleep(10)

strip.cleanup()