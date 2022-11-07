import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

motor =4

GPIO.setup(4, GPIO.OUT) 
GPIO.output(4, GPIO.HIGH)

while(True):
  try:
    GPIO.output(4, GPIO.LOW)
    print("ONE")
    time.sleep(2)

  except KeyboardInterupt:
   break
