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
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import random

#from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

#client = TBDeviceMqttClient(config.THINGSBOARD_HOST, port=config.THINGSBOARD_MQTT_PORT, username=config.THINGSBOARD_MQTT_USERNAME, password=config.THINGSBOARD_MQTT_PASSWORD, client_id=config.THINGSBOARD_MQTT_CLIENT_ID)

i2c_1 = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c_1)
lcd = LCD(bus=3)

channel_0 = AnalogIn(ads, ADS.P0)
channel_1 = AnalogIn(ads, ADS.P1)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-030794972bbe')[0]
device_file = device_folder + '/w1_slave'

GPIO.setmode(GPIO.BCM)

def safe_exit(signum, frame):
    exit(1)

#def display(temp,ph,tds):
#  signal(SIGTERM, safe_exit)
#  signal(SIGHUP, safe_exit)
#  lcd.text("Suhu={} pH={}".format(temp,ph),1,'centre')
#  lcd.text("TDS={}".format(tds),2,'centre')

#def pump(ppm,base):
#    if ppm<=1050:
#      GPIO.setup(17, GPIO.OUT) 
#      GPIO.output(17, GPIO.HIGH)
#      time.sleep(2)
#      GPIO.output(17, GPIO.LOW)
#      time.sleep(1)
#      GPIO.output(17, GPIO.HIGH)
      # print("ONE")
      #GPIO.cleanup()
#    if base>=7:
      #case if two relay channel activated
#      GPIO.setup(18, GPIO.OUT) 
#      GPIO.output(18, GPIO.HIGH)
#      time.sleep(1) 
#      GPIO.output(18, GPIO.LOW)
#      time.sleep(1)
#      GPIO.output(18, GPIO.HIGH)
      # print("TWO")
      #GPIO.cleanup()
#    if ppm>1050 or base < 7:
#      GPIO.output(17, GPIO.HIGH)
#      GPIO.output(18, GPIO.HIGH)
      #GPIO.cleanup()
      
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_sensor():
    while True:
      
      #temperature
      
      lines = read_temp_raw()
      while lines[0].strip()[-3:] != 'YES':
          time.sleep(0.2)
          lines = read_temp_raw()
      equals_pos = lines[1].find('t=')
      if equals_pos != -1:
          temp_string = lines[1][equals_pos+2:]
          temp_c = round((float(temp_string) / 1000.0),2)
          temp_f = temp_c * 9.0 / 5.0 + 32.0
      
      
      #pH
          
      
      buf_1 = list()
      for i in range(10): # Take 10 samples
            #buf_1.append(random.uniform(7.0, 8.0))
            buf_1.append(channel_0.voltage)
      buf_1.sort() # Sort samples and discard highest and lowest
      buf_1 = buf_1[2:-2]
      avg = round((sum(map(float,buf_1))/6),2) # Get average value from remaining 6
      #avg = (sum(map(float,buf_1))/6)
      #pH=round((-7.308*avg+33.443),1)
      #pH = 3.5*(avg*5/1024/6)
      # pH= round((-8.475*avg+38.7575),2)
      
    
      #tds

      buf_0 = list()
      for i in range(10): # Take 10 samples
          buf_0.append(channel_1.voltage)
      buf_0.sort() # Sort samples and discard highest and lowest
      buf_0 = buf_0[2:-2]
      raw = round((sum(map(float,buf_0))/6),2)
      compensation_coefficient = 1.0+0.02*(temp_c-25.0)
      compensation_voltage = raw/compensation_coefficient
      tds = (133.42*compensation_voltage*compensation_voltage*compensation_voltage - 255.86*compensation_voltage*compensation_voltage + 857.39*compensation_voltage)*0.5
      
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
      #display(temp_c,pH,tds)
     # pump(tds,pH)
      time.sleep(2) 

while True:
 print(read_sensor())
 time.sleep(1)
