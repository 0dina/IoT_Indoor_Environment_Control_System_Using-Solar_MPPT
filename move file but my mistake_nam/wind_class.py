import board
import busio
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.analog_in import AnalogIn

class WindDirectionSensor:
    def __init__(self):
        # Initialize I2C bus and ADS1015
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS1015(i2c)

    def read_wind_direction(self):
        # Read from channel 0
        channel = AnalogIn(self.ads, 0)
        voltage = channel.voltage
        return voltage

    def print_wind_direction(self):
        # Print the wind direction voltage
        voltage = self.read_wind_direction()
        print(f"Wind Direction Voltage: {voltage:.2f}V")
