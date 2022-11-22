from capstone.main import SmartHydroponic
import time

controller = SmartHydroponic()

while (True):
    print(controller.read_sensor())
    time.sleep(1)