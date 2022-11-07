import os
import time
import picamera
from datetime import datetime
import base64
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from config import config
import io
from PIL import Image

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.start_preview()

client = TBDeviceMqttClient(config.THINGSBOARD_HOST, port=config.THINGSBOARD_MQTT_PORT, username=config.THINGSBOARD_MQTT_USERNAME, password=config.THINGSBOARD_MQTT_PASSWORD, client_id=config.THINGSBOARD_MQTT_CLIENT_ID)
# Connect to ThingsBoard
client.connect()

while True:
    camera_output = io.BytesIO()
    camera.capture(camera_output, format="jpeg")

    image = Image.open(camera_output)
    image = image.resize((320,180), Image.ANTIALIAS)

    camera_output = io.BytesIO()
    image.save(camera_output, optimize=True, quality=70, format="jpeg")

    camera_output_encoded = base64.b64encode(camera_output.getvalue())

    telemetry = {
        "camera_encoded" : camera_output_encoded.decode(),
    }

    client.send_telemetry(telemetry)
    print("test")
    time.sleep(2.0) 