import time
import adafruit_vl53l0x
from adafruit_extended_bus import ExtendedI2C as I2C

i2c = I2C(1)

sensor = adafruit_vl53l0x.VL53L0X(i2c)

print("VL53L0X ready")

while True:
    distance = sensor.range
    print(f"Distance: {distance} mm")
    time.sleep(0.2)