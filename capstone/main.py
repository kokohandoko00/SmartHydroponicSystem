import os
import glob
import time
import board
import busio
import sys
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import config
import RPi.GPIO as GPIO
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import random

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
GPIO.setmode(GPIO.BCM)

LAMP_PIN = 17
PH_PIN = 27
TDS_PIN = 18

class SmartHydroponic(object):
    """
    Capstone Smart Hydroponic object
    """

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.lcd = LCD(bus=3)
        self.channel_0 = AnalogIn(self.ads, ADS.P3)
        self.channel_1 = AnalogIn(self.ads, ADS.P1)

        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28-030794972bbe')[0]
        self.device_file = self.device_folder + '/w1_slave'

    def safe_exit(self, signum, frame):
        exit(1)

    def display(self, temp, ph, tds):
        signal(SIGTERM, self.safe_exit)
        signal(SIGHUP, self.safe_exit)
        self.lcd.text("Suhu={} pH={}".format(temp, ph),1,'centre')
        self.lcd.text("TDS={}".format(tds),2,'centre')

    def pump(self, ppm, base):
        print(f"ppm {ppm} base {base}")
        if ppm<=1050:
            GPIO.setup(TDS_PIN, GPIO.OUT) 
            GPIO.output(TDS_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(TDS_PIN, GPIO.LOW)
            time.sleep(1)
            GPIO.output(TDS_PIN, GPIO.HIGH)
            # print("ONE")
            #GPIO.cleanup()
        if base>=9.0:
            #case if two relay channel activated
            GPIO.setup(PH_PIN, GPIO.OUT) 
            GPIO.output(PH_PIN, GPIO.HIGH)
            time.sleep(1) 
            GPIO.output(PH_PIN, GPIO.LOW)
            time.sleep(1)
            GPIO.output(PH_PIN, GPIO.HIGH)
            # print("TWO")
            #GPIO.cleanup()
        if ppm>1050 or base < 7:
            GPIO.output(TDS_PIN, GPIO.HIGH)
            GPIO.output(PH_PIN, GPIO.HIGH)
            #GPIO.cleanup()
      
    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = round((float(temp_string) / 1000.0),2)
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c
        return 0
    
    def read_pH(self):
        buf_1 = list()
        for i in range(10): # Take 10 samples
                buf_1.append(random.uniform(7.0, 8.0))
                #buf_1.append(self.channel_1.voltage)
        buf_1.sort() # Sort samples and discard highest and lowest
        buf_1 = buf_1[2:-2]
        avg = round((sum(map(float,buf_1))/6),2) # Get average value from remaining 6
        pH = avg
        # pH= round((-8.475*avg+38.7575),2)
        return pH

    def read_tds(self):
        buf_0 = list()
        for i in range(10): # Take 10 samples
            buf_0.append(self.channel_0.voltage)
        buf_0.sort() # Sort samples and discard highest and lowest
        buf_0 = buf_0[2:-2]
        raw = round((sum(map(float,buf_0))/6),2)
        tds = raw
        # tds = round((1395*raw-1776.35),2)

        return tds
        

    def read_sensor(self):
        
        #temperature
        
        temp_c = self.read_temp()
        
        #pH
        
        pH = self.read_pH()
        
        #tds

        tds = self.read_tds()
        
        print(f"Suhu dalam Celcius = {temp_c}")
        # print("Suhu dalam Fahrenheit={}".format(temp_f))
        print(f"pH Air = {pH}")
        print(f"TDS = {tds}")

        # telemetry = {
        #   "temperature" : temp_c,
        #   "pH" : pH,
        #   "TDS" : tds,
        # }
        # client.send_telemetry(telemetry)
        self.display(temp_c,pH,tds)
        self.pump(tds, pH)
        time.sleep(2) 