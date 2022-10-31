import picamera 
from time import sleep

camera=picamera.PiCamera()

camera.start_preview()
sleep(5)
camera.capture('Desktop/image3.jpg')
camera.stop_preview()
