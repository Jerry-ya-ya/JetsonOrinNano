import serial
from pynput import mouse

SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE = 115200

def init_serial():
    ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, dsrdtr=None)
    ser.setRTS(False)
    ser.setDTR(False)
    return ser

def send_forward(ser):
    command = '{"T":1,"L":0.5,"R":0.5}'
    ser.write(command.encode("utf-8") + b"\n")
    print(">>> FORWARD <<<", command)

def send_stop(ser):
    command = '{"T":1,"L":0,"R":0}'
    ser.write(command.encode("utf-8") + b"\n")
    print(">>> STOP <<<", command)

def on_click(x, y, button, pressed):
    global ser

    if button == mouse.Button.left:
        if pressed:
            send_forward(ser)
        else:
            send_stop(ser)

ser = init_serial()

listener = mouse.Listener(on_click=on_click)
listener.start()

print("滑鼠左鍵按下前進，放開停止。按 Ctrl+C 離開。")

try:
    listener.join()
except KeyboardInterrupt:
    pass
finally:
    ser.close()