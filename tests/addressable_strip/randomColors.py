from apa102_pi.driver import apa102
from time import sleep, time
import RPi.GPIO as GPIO
import signal
import random
import sys

strip = apa102.APA102(num_led=144, order='rgb')
strip2 = apa102.APA102(num_led=144, order='rgb', mosi=20, sclk=21)
motor = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor,GPIO.OUT)

def cleanStrip(sig, frame):
  global strip, strip2
  strip.cleanup()
  strip2.cleanup()
  GPIO.setup(motor,0)
  GPIO.output(motor, GPIO.LOW)
  GPIO.cleanup()
  sys.exit(0)

signal.signal(signal.SIGINT, cleanStrip)

def randomColors(strips, delay):
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    c = (int(r), int(g), int(b))
    for strip in strips:
      for i in range(48):
        strip.set_pixel_rgb(i, c[0]<<16|c[1]<<8|c[2])
      strip.show()
    sleep(delay)

GPIO.output(motor, GPIO.HIGH)
while True:
  randomColors((strip,strip2),1)
