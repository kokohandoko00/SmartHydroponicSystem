#!/usr/bin/python
''' Raspberry Pi, ADS1115, PH4502C Calibration '''
import board
import busio
import time
import sys
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Setup 
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

def read_voltage(channel):
    while True:
        buf = list()
        
        for i in range(10): # Take 10 samples
            buf.append(channel.voltage)
        buf.sort() # Sort samples and discard highest and lowest
        buf = buf[2:-2]
        avg = round((sum(map(float,buf))/6),2) # Get average value from remaining 6
        #pH = (-8.475*avg+38.7575)
        pH=(-8.475*avg+38.7575)
        print(round(pH,2))
        #print(avg)
        time.sleep(2)

if __name__ == '__main__':
    print('\n\n\n')
    print('---- RPi-ADS115-PH4502 Calibration ----')
    input('Press Enter once you have grounded the BNC connector...')
    channel = None
    while channel not in [0,1,2,3]:
        try: 
            channel = int(input('ADS1115 channel 0-3: '))  # ADS.P0, ADS.P1, ADS.P2, ADS.P3
        except:
            print('Not a valid option. Try again.')
    if channel == 0:
        channel = AnalogIn(ads, ADS.P0)
    elif channel == 1:
        channel = AnalogIn(ads, ADS.P1)
    elif channel == 2:
        channel = AnalogIn(ads, ADS.P1)
    elif channel == 3:
        channel = AnalogIn(ads, ADS.P1)
    else:
        sys.exit('Error selecting an ADS1115 pin.')
    print('Adjust potentiometer nearest to BNC socket to ~2.50V')
    print('Starting readings. Press CTRL+C to stop...')
    try:
        read_voltage(channel)
    except KeyboardInterrupt:
        pass
