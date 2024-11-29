import math
import board
import time
from adafruit_bme280 import basic as adafruit_bme280

class BME280Sensor:
    def __init__(self, measured_pressure=1018.0, target_altitude=15.0, temperature_celsius=25.0):
        # Constants
        self.R = 287.05  # Gas constant (J/(kg·K))
        self.g = 9.80665  # Gravitational acceleration (m/s²)

        # Inputs
        self.P = measured_pressure  # Measured pressure (hPa)
        self.h_target = target_altitude  # Target altitude (m)
        self.T_celsius = temperature_celsius  # Temperature in Celsius

        # Calculate temperature in Kelvin
        self.T_kelvin = self.T_celsius + 273.15

        # Calculate new sea level pressure (P0)
        self.P0_new = self.P * math.exp((self.g * self.h_target) / (self.R * self.T_kelvin))

        # I2C 통신 초기화
        i2c = board.I2C()
        self.sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c)

        # Set sea level pressure
        self.sensor.sea_level_pressure = self.P0_new

    def read_temperature(self):
        return self.sensor.temperature

    def read_humidity(self):
        return self.sensor.humidity

    def read_pressure(self):
        return self.sensor.pressure

    def read_altitude(self):
        return self.sensor.altitude

    def print_readings(self):
        print(f"Temperature: {self.read_temperature():.1f} °C")
        print(f"Humidity: {self.read_humidity():.1f} %")
        print(f"Pressure: {self.read_pressure():.1f} hPa")
        print(f"Altitude: {self.read_altitude():.2f} m")
        print()