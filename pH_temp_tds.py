import os
import glob
import time
import board
import busio
import sys
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import Adafruit_ADS1x15


i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
adc = Adafruit_ADS1x15.ADS1115()
gain=2/3
adc.start_adc(0,gain) 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-030794972bbe')[0]
device_file = device_folder + '/w1_slave'

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
      channel = AnalogIn(ads, ADS.P1)
      buf = list()
      for i in range(10): # Take 10 samples
          buf.append(channel.voltage)
      buf.sort() # Sort samples and discard highest and lowest
      buf = buf[2:-2]
      avg = round((sum(map(float,buf))/6),2) # Get average value from remaining 6
      pH= round((-8.475*avg+38.7575),2)
      #tds
      channel1 = AnalogIn(ads, ADS.P0)
      buff = list()
      for i in range(10): # Take 10 samples
          buff.append(channel1.voltage)
      buff.sort() # Sort samples and discard highest and lowest
      buff = buff[2:-2]
      tds = round((sum(map(float,buff))/6),2)
      print("Suhu dalam Celcius={}".format(temp_c))
      print("Suhu dalam Fahrenheit={}".format(temp_f))
      print("pH Air={}".format(pH))
      print("TDS={}".format(tds))
      time.sleep(2)

while True:
 print(read_temp())
 time.sleep(1)
