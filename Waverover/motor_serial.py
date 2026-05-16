import time
import serial

from config import SERIAL_PORT, BAUDRATE
from pynput import keyboard

from config import TURN_DEADZONE

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

def send_drive(ser, left, right):
    if ser is None:
        print("Serial is not available")
        return

    left = apply_deadzone_compensation(left, TURN_DEADZONE)
    right = apply_deadzone_compensation(right, TURN_DEADZONE)

    command = f'{{"T":1,"L":{left:.2f},"R":{right:.2f}}}'
    ser.write(command.encode("utf-8") + b"\n")
    ser.flush()
    print(">>> DRIVE <<<", command)

def apply_deadzone_compensation(value, deadzone):
    if value == 0:
        return 0

    if value > 0:
        return deadzone + value * (0.5 - deadzone) / 0.5

    return -deadzone + value * (0.5 - deadzone) / 0.5

def send_forward(ser):
    send_drive(ser, 0.2, 0.2)

def send_stop(ser):
    send_drive(ser, 0, 0)

def trigger_stop(ser):
    if ser is None:
        print(">>> STOP COMMAND TRIGGERED <<< but serial is not available")
        return
    send_stop(ser)
    print(">>> STOP COMMAND TRIGGERED <<<")

def get_keyboard_drive(keyboard_controller):
    speed = 0.35
    turn_speed = 0.3

    if keyboard_controller.is_pressed(keyboard.Key.w):
        return speed, speed

    if keyboard_controller.is_pressed(keyboard.Key.s):
        return -speed, -speed

    if keyboard_controller.is_pressed(keyboard.Key.a):
        return -turn_speed, turn_speed

    if keyboard_controller.is_pressed(keyboard.Key.d):
        return turn_speed, -turn_speed

    return 0, 0