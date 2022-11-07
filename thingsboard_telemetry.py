from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from config import config

telemetry = {
    "temperature" : 32.0,
    "pH" : 4.1,
    "TDS" : 1000.24,
}
client = TBDeviceMqttClient(config.THINGSBOARD_HOST, port=config.THINGSBOARD_MQTT_PORT, username=config.THINGSBOARD_MQTT_USERNAME, password=config.THINGSBOARD_MQTT_PASSWORD, client_id=config.THINGSBOARD_MQTT_CLIENT_ID)
# Connect to ThingsBoard
client.connect()
# Sending telemetry without checking the delivery status
client.send_telemetry(telemetry) 
# Sending telemetry and checking the delivery status (QoS = 1 by default)
result = client.send_telemetry(telemetry)
# get is a blocking call that awaits delivery status  
success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
# Disconnect from ThingsBoard
client.disconnect()