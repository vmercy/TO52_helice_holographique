#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
addressable_strip/main.py: Draft script aiming to test an addressable LED strip with following reference: sj-100144-102
"""
from apa102_pi.driver import apa102
from time import sleep
import signal
import sys

strip = apa102.APA102(num_led=144, order='rgb')

""" def signal_handler(sig, frame):
    global strip
    print('Extinction du bandeau')
    strip.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler) """

strip.clear_strip()

nbLeds = 144
startFreq = sys.argv[0]
freqMax = 1000
dureeFixe = 1
for freq in range(startFreq,freqMax):
  delay = (1/freq)/2
  print(freq)
  duree = dureeFixe
  while(duree>=0):
    for i in range(nbLeds):
      strip.set_pixel_rgb(i,  0xFFFFFF)
    strip.show()
    sleep(delay)
    for i in range(nbLeds):
      strip.set_pixel_rgb(i,  0x000000)
    strip.show()
    sleep(delay)
    duree-=2*delay

strip.cleanup()