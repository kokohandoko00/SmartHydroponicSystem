import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

tds=1000
pH=7

while(True):
  try:
    if tds<=1000:
      GPIO.setup(17, GPIO.OUT) 
      GPIO.output(17, GPIO.HIGH)
      GPIO.output(17, GPIO.LOW)
      print("ONE")
      time.sleep(2)
    if pH>=9:
      #case if two relay channel activated
      GPIO.setup(27, GPIO.OUT) 
      GPIO.output(27, GPIO.HIGH)
      GPIO.output(27, GPIO.LOW)
      GPIO.setup(22, GPIO.OUT) 
      GPIO.output(22, GPIO.HIGH)
      GPIO.output(22, GPIO.LOW)
      print("TWO")
      time.sleep(2)
      #case if only one relay channel activated. with this option, it should have configured on wire
      # GPIO.setup(27, GPIO.OUT) 
      # GPIO.output(27, GPIO.HIGH)
      # GPIO.output(27, GPIO.LOW)
      # print("TWO")
      # time.sleep(2)


  except KeyboardInterupt:
   break
