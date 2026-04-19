import time
import serial

from config import SERIAL_PORT, BAUDRATE

def init_serial():
    try:
        print(f"[INFO] Opening serial port: {SERIAL_PORT} @ {BAUDRATE}")
        ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=1, dsrdtr=None)
        ser.setRTS(False)
        ser.setDTR(False)
        time.sleep(0.5)
        return ser
    except Exception as e:
        print(f"[ERROR] Failed to open serial port: {e}")
        return None

def send_forward(ser):
    command = '{"T":1,"L":0.2,"R":0.2}'
    ser.write(command.encode("utf-8") + b"\n")
    ser.flush()
    print(">>> FORWARD <<<", command)

def send_stop(ser):
    command = '{"T":1,"L":0,"R":0}'
    ser.write(command.encode("utf-8") + b"\n")
    ser.flush()
    print(">>> STOP <<<", command)

def trigger_stop(ser):
    if ser is None:
        print(">>> STOP COMMAND TRIGGERED <<< but serial is not available")
        return
    send_stop(ser)
    print(">>> STOP COMMAND TRIGGERED <<<")