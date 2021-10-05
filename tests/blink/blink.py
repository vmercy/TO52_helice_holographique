#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
blink/main.py: Script that makes an LED blink
"""

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

ledPin = 18
delay = 0.1

GPIO.setup(ledPin, GPIO.OUT)

while(1):
  GPIO.output(ledPin, GPIO.HIGH)
  sleep(delay)
  GPIO.output(ledPin, GPIO.LOW)
  sleep(delay)