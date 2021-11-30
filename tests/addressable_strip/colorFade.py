from apa102_pi.driver import apa102
from time import sleep, time
import RPi.GPIO as GPIO
import signal
import sys

strip = apa102.APA102(num_led=144, order='rgb')
strip2 = apa102.APA102(num_led=144, order='rgb', mosi=20, sclk=21)

# Helper for converting 0-255 offset to a colour tuple
def wheel(offset, brightness):
    # The colours are a transition r - g - b - back to r
    offset = 255 - offset
    if offset < 85:
        return (255 - offset * 3, 0, offset * 3, brightness)
    if offset < 170:
        offset -= 85
        return (0, offset * 3, 255 - offset * 3, brightness)
    offset -= 170
    return (offset * 3, 255 - offset * 3, 0, brightness)


def colorFade(strip, colorFrom, colorTo, wait_ms=20, steps=10):
    for r in range(5):
      for n in range(256):
          for i in range(strip.n):
              strip[i] = wheel(((i * 256 // strip.n) + n) & 255, 255)
          strip.write()
      time.sleep_ms(25)

colorFade(strip, (255,0,255),(0,255,0))