import os
import glob
import time
import board
import busio
import sys
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from config import config
import RPi.GPIO as GPIO

#from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

#client = TBDeviceMqttClient(config.THINGSBOARD_HOST, port=config.THINGSBOARD_MQTT_PORT, username=config.THINGSBOARD_MQTT_USERNAME, password=config.THINGSBOARD_MQTT_PASSWORD, client_id=config.THINGSBOARD_MQTT_CLIENT_ID)

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

channel_0 = AnalogIn(ads, ADS.P0)
channel_1 = AnalogIn(ads, ADS.P1)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-030794972bbe')[0]
device_file = device_folder + '/w1_slave'

GPIO.setmode(GPIO.BCM)

def pump(ppm,base):
    if ppm<=1050:
      GPIO.setup(17, GPIO.OUT) 
      GPIO.output(17, GPIO.LOW)
      time.sleep(2)
      GPIO.output(17, GPIO.HIGH)
      print("ONE")
      #GPIO.cleanup()
    if base>=9:
      #case if two relay channel activated
      GPIO.setup(27, GPIO.OUT) 
      GPIO.output(27, GPIO.LOW)
      time.sleep(1) 
      GPIO.output(27, GPIO.HIGH)
      print("TWO")
      # GPIO.cleanup()
    #if KeyboardInterrupt:
      #  GPIO.cleanup()
      
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    while True:
      
      #temperature
      
      lines = read_temp_raw()
      while lines[0].strip()[-3:] != 'YES':
          time.sleep(0.2)
          lines = read_temp_raw()
      equals_pos = lines[1].find('t=')
      if equals_pos != -1:
          temp_string = lines[1][equals_pos+2:]
          temp_c = float(temp_string) / 1000.0
          temp_f = temp_c * 9.0 / 5.0 + 32.0
      
      
      #pH
      
      buf_1 = list()
      for i in range(10): # Take 10 samples
          buf_1.append(channel_1.voltage)
      buf_1.sort() # Sort samples and discard highest and lowest
      buf_1 = buf_1[2:-2]
      avg = round((sum(map(float,buf_1))/6),2) # Get average value from remaining 6
      pH= round((-8.475*avg+38.7575),2)
      
    
      #tds

      buf_0 = list()
      for i in range(10): # Take 10 samples
          buf_0.append(channel_0.voltage)
      buf_0.sort() # Sort samples and discard highest and lowest
      buf_0 = buf_0[2:-2]
      raw = round((sum(map(float,buf_0))/6),2)
      tds = round((407.27*raw+56.2642),2)
      
      print("Suhu dalam Celcius={}".format(temp_c))
      print("Suhu dalam Fahrenheit={}".format(temp_f))
      print("pH Air={}".format(pH))
      print("TDS={}".format(tds))

     # telemetry = {
     #   "temperature" : temp_c,
     #   "pH" : pH,
     #   "TDS" : tds,
     # }

     # client.send_telemetry(telemetry)
      pump(tds,pH)
      time.sleep(2) 

while True:
 print(read_temp())
 time.sleep(1)
