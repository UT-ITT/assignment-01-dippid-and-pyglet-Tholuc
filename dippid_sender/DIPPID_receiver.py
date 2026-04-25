import time
from DIPPID import SensorUDP # type: ignore

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

def handle_data(data):
    print(data)

sensor.register_callback('accelerometer', handle_data)
sensor.register_callback('button_1', handle_data)

while True:
    time.sleep(10)



