import socket
import time
import math
import random
import json

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

t = 0  # time variable
button_1 = 0 # button starts unpressed

while True:
    # Simulate accelerometer with sine waves and some noise 
    acc_x = math.sin(t) + random.gauss(0, 0.07)
    acc_y = math.sin(t * 0.5) + random.gauss(0, 0.05)
    acc_z = math.sin(t * 0.25) + random.gauss(0, 0.03)

    # Simulate button (random press/release chance at 20%)
    if random.random() < 0.2:
        button_1 = 1 - button_1

    # Create message in DIPPID/dictionary format
    message = {
        "accelerometer": [acc_x, acc_y, acc_z],
        "button_1": button_1
    }

    # Convert to JSON
    message_str = json.dumps(message)
    print(message_str)

    # Send via UDP
    sock.sendto(message_str.encode(), (IP, PORT))

    # Increase time
    t += 0.1

    # 1 message every 10th of a second
    time.sleep(0.1)