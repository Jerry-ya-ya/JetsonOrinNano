import serial
import json
import time

SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
time.sleep(2)

data = {"T": 1, "L": 0.2, "R": 0.2}
command = json.dumps(data) + "\n"
ser.write(command.encode("utf-8"))
ser.flush()
print("sent:", command)

time.sleep(2)

data = {"T": 1, "L": 0.0, "R": 0.0}
command = json.dumps(data) + "\n"
ser.write(command.encode("utf-8"))
ser.flush()
print("sent:", command)

ser.close()