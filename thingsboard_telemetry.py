from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from config import config
import random
import time
import RPi.GPIO as GPIO

LAMP_PIN = 17

lamp_state = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(LAMP_PIN, GPIO.OUT) 

def on_server_side_rpc_request(request_id, request_body):
    print(request_id, request_body)
    if request_body["method"] == "getLampValue":
        client.send_rpc_reply(request_id, lamp_state)
    elif request_body["method"] == "setLampValue":
        lamp_state = request_body["params"]
        GPIO.output(LAMP_PIN, GPIO.LOW if lamp_state else GPIO.HIGH)
        client.send_rpc_reply(request_id, lamp_state)


client = TBDeviceMqttClient(config.THINGSBOARD_HOST, port=config.THINGSBOARD_MQTT_PORT, username=config.THINGSBOARD_MQTT_USERNAME, password=config.THINGSBOARD_MQTT_PASSWORD, client_id=config.THINGSBOARD_MQTT_CLIENT_ID)
# Connect to ThingsBoard
client.set_server_side_rpc_request_handler(on_server_side_rpc_request)
client.connect()

while True:
    telemetry = {
        "temperature" : random.uniform(15.0, 40.0),
        "pH" : random.uniform(7.0, 8.0),
        "TDS" : random.uniform(0.0, 1000.0),
    }
    client.send_telemetry(telemetry)
    print(telemetry) 
    time.sleep(4.0)
    

# Sending telemetry without checking the delivery status
# Sending telemetry and checking the delivery status (QoS = 1 by default)
# result = client.send_telemetry(telemetry)
# get is a blocking call that awaits delivery status  
# success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
# Disconnect from ThingsBoard
client.disconnect()
