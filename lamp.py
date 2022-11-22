import RPi.GPIO as GPIO
import time

LAMP_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LAMP_PIN, GPIO.OUT) 
GPIO.output(LAMP_PIN, GPIO.LOW)
time.sleep(2)
GPIO.output(LAMP_PIN, GPIO.HIGH)
