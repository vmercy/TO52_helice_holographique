import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)

while(True):
  near = GPIO.input(27)
  print(near)