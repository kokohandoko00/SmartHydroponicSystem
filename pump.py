import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

tds=1000
pH=8

# ph=7
# tds=1050<=tds<=1400

while(True):
  try:
    if tds<=1050:
      GPIO.setup(17, GPIO.OUT) 
      GPIO.output(17, GPIO.LOW)
      time.sleep(200)
      GPIO.output(17, GPIO.HIGH)
      print("ONE")
      #GPIO.cleanup()
    if pH>=9:
      #case if two relay channel activated
      GPIO.setup(27, GPIO.OUT) 
      GPIO.output(27, GPIO.LOW)
      time.sleep(1) 
      GPIO.output(27, GPIO.HIGH)
      #GPIO.setup(22, GPIO.OUT) 
      #GPIO.output(22, GPIO.HIGH)
      #GPIO.output(22, GPIO.LOW)
      print("TWO")
      GPIO.cleanup()
      #case if only one relay channel activated. with this option, it should have configured on wire
      # GPIO.setup(27, GPIO.OUT) 
      # GPIO.output(27, GPIO.HIGH)
      # GPIO.output(27, GPIO.LOW)
      # print("TWO")
      # time.sleep(2)


  except KeyboardInterrupt:
   GPIO.cleanup()
   break
