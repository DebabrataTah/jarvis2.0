import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.IN)

def MOTION(PIR_PIN):
  print "1"

time.sleep(2)

GPIO.add_event_detect(8, GPIO.RISING, callback=MOTION)
while 1:
  time.sleep(1)



