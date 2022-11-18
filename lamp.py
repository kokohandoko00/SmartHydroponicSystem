import RPi.GPIO as GPIO
import time
from apscheduler.schedulers.blocking import BlockingScheduler

def lamp_on():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT) 
    GPIO.output(17, GPIO.LOW)
    time.sleep(2)
    GPIO.output(17, GPIO.HIGH)

scheduler = BlockingScheduler()
scheduler.reschedule_job('lamp_on', trigger='cron', minute='018***')