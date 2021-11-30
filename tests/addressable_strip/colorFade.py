from apa102_pi.driver import apa102
from time import sleep, time
import RPi.GPIO as GPIO
import signal
import sys

strip = apa102.APA102(num_led=144, order='rgb')
strip2 = apa102.APA102(num_led=144, order='rgb', mosi=20, sclk=21)

def colorFade(strip, colorFrom, colorTo, wait_ms=20, steps=10):
    steps = 200

    step_R = int(colorTo[0]) / steps
    step_G = int(colorTo[1]) / steps
    step_B = int(colorTo[2]) / steps
    r = int(colorFrom[0])
    g = int(colorFrom[1])
    b = int(colorFrom[2])

    for x in range(steps):
        c = (int(r), int(g), int(b))
        for i in range(48):
            strip.set_pixel_rgb(i, r<<16|g<<8|b)
        strip.show()
        sleep(wait_ms / 1000.0)
        r += step_R
        g += step_G
        b += step_B

colorFade(strip, (255,0,255),(0,255,0))