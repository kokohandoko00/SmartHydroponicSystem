import os
import time
import picamera
from datetime import datetime

d = datetime.now()
initYear = "%04d" % (d.year)
initMonth = "%02d" % (d.month)
initDate = "%02d" % (d.day)
initHour = "%02d" % (d.hour)
initMins = "%02d" % (d.minute)
initSecs = "%02d" % (d.second)

CameraTimeLapse = "timelapse_" + str(initYear) + str(initMonth) + str(initDate) +"_"+ str(initHour) + str(initMins)
os.mkdir(CameraTimeLapse)

# initial set
fileSerial = 1

# Create and configure the camera, adjustTime= camera preparation
adjustTime=5
pauseBetweenShots=600000

# Create and configure the camera
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    #camera.exposure_compensation = 5

    # Start the preview and give the camera a couple of seconds to adjust
    camera.start_preview()
    try:
        time.sleep(adjustTime)

        start = time.time()
        while True:
            d = datetime.now()
            fileSerialNumber = "%04d" % (fileSerial)

            # Capture the CURRENT time (not start time as set above) to insert into each capture image filename
            hour = "%02d" % (d.hour)
            mins = "%02d" % (d.minute)
            secs = "%02d" % (d.second)
            camera.capture(str(CameraTimeLapse) + "/" + str(fileSerialNumber) + "_" + str(hour) + str(mins) + str(secs) + ".jpg")

            fileSerial += 1
            time.sleep(pauseBetweenShots)

    except KeyboardInterrupt:
        print ('interrupted!')
        # Stop the preview and close the camera
        camera.stop_preview()

finish = time.time()
print("Captured %d images in %d seconds" % (fileSerial,finish - start))
