from apa102_pi.driver import apa102
import time
import RPi.GPIO as GPIO
import signal
import random
import sys

strip = apa102.APA102(num_led=48, order='rgb')
strip2 = apa102.APA102(num_led=48, order='rgb', mosi=20, sclk=21)
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

GPIO.output(motor, GPIO.HIGH)
print(sys.argv)
while True:
  for i in range(48):
    strip.set_pixel_rgb(i,0xFF0000)
  strip.show()
  #time.sleep(0.001)
  strip.clear_strip()
  time.sleep(float(sys.argv[1]))
