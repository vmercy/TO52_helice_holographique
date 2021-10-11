#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
blink/main.py: Script that makes an LED blink
"""

import RPi.GPIO as GPIO
import time

servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
time.sleep(2)
p.start(2.5) # Initialization
print('Starting motor')
try:
  while True:
    p.ChangeDutyCycle(50)
    time.sleep(0.5)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()