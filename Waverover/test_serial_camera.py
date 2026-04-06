import serial
import time

ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, dsrdtr=None)
ser.setRTS(False)
ser.setDTR(False)

command = '{"T":1,"L":0,"R":0}'
ser.write(command.encode("utf-8") + b"\n")
print("sent:", command)

time.sleep(1)
ser.close()