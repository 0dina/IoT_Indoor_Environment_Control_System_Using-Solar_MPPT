import board
import busio
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS1015(i2c)

def read_wind_direction():
    channel = AnalogIn(ads,0)
    voltage = channel.voltage
    print(f"Winf\d Direction Voltage: {voltage:.2f}V")

read_wind_direction()