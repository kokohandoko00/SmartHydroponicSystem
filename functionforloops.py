# def suhu():
#     return print(1)
# def tds():
#     return print(2)
# def ph():
#     return print(3)

# def call():
#     f = (suhu, tds, ph)
#     for func in f:
#         print(func)

# import random
import time

# def read_temp(self):
#         lines = self.read_temp_raw()
#         while lines[0].strip()[-3:] != 'YES':
#             time.sleep(0.2)
#             lines = self.read_temp_raw()
#         equals_pos = lines[1].find('t=')
#         if equals_pos != -1:
#             temp_string = lines[1][equals_pos+2:]
#             temp_c = round((float(temp_string) / 1000.0),2)
#             # temp_f = temp_c * 9.0 / 5.0 + 32.0
#             return temp_c
#         return 0
    
# def read_pH(self):
#         buf_1 = list()
#         for i in range(10): # Take 10 samples
#                 buf_1.append(random.uniform(7.0, 8.0))
#                 #buf_1.append(self.channel_1.voltage)
#         buf_1.sort() # Sort samples and discard highest and lowest
#         buf_1 = buf_1[2:-2]
#         avg = round((sum(map(float,buf_1))/6),2) # Get average value from remaining 6
#         pH = avg
#         # pH= round((-8.475*avg+38.7575),2)
#         return pH, avg

# def read_tds(self, temperature):
#         buf_0 = list()
#         for i in range(10): # Take 10 samples
#             buf_0.append(self.channel_0.voltage)
#         buf_0.sort() # Sort samples and discard highest and lowest
#         buf_0 = buf_0[2:-2]
#         raw = round((sum(map(float,buf_0))/6),2)
#         tds = raw
#         # tds = round((1360.45*raw-1070.29),2)
#         compensation_coefficient = 1.0+0.02*(temperature-25.0)
#         compensation_voltage = raw/compensation_coefficient
#         tds = (133.42*compensation_voltage*compensation_voltage*compensation_voltage - 255.86*compensation_voltage*compensation_voltage + 857.39*compensation_voltage)*0.5

#         return tds, raw

# def ph_relay():
#     GPIO.output(TDS_PIN, GPIO.HIGH)
#     time.sleep(1)
#     GPIO.output(TDS_PIN, GPIO.LOW)
#     time.sleep(1)
#     GPIO.output(TDS_PIN, GPIO.HIGH)

# def tds_relay():
#     GPIO.output(PH_PIN, GPIO.HIGH)
#     time.sleep(1) 
#     GPIO.output(PH_PIN, GPIO.LOW)
#     time.sleep(1)
#     GPIO.output(PH_PIN, GPIO.HIGH)

while True:
    b="on"
    c="off"
    a=(b,c)
    for func in a:
        if func == b:
            print(2)
            time.sleep(2)
        if func == c:
            print(3)
            time.sleep(2)



