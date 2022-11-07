import os
import time
import picamera
from datetime import datetime
import base64
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from config import config
import io

camera = picamera.PiCamera()
camera.resolution = (1280, 720)

client = TBDeviceMqttClient(config.THINGSBOARD_HOST, port=config.THINGSBOARD_MQTT_PORT, username=config.THINGSBOARD_MQTT_USERNAME, password=config.THINGSBOARD_MQTT_PASSWORD, client_id=config.THINGSBOARD_MQTT_CLIENT_ID)
# Connect to ThingsBoard
client.connect()

while True:
    camera_output = io.BytesIO()
    camera.capture(camera_output, format="jpeg")

    camera_output_encoded = base64.b64encode(camera_output.getvalue())

    telemetry = {
        "camera_encoded" : camera_output_encoded,
    }

    client.send_telemetry(telemetry) 