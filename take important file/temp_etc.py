import time
import board
import math
from adafruit_bme280 import basic as adafruit_bme280

# Constants   ///  calculate for Altitude adapt normalvalue
R = 287.05  # Gas constant (J/(kg·K))
g = 9.80665  # Gravitational acceleration (m/s²)

# Inputs
P = 1018.0  # Measured pressure (hPa)
h_target = 15.0  # Target altitude (m)
T_celsius = 25.0  # Temperature in Celsius

# Convert temperature to Kelvin
T_kelvin = T_celsius + 273.15

# Calculate new sea level pressure (P0)
P0_new = P * math.exp((g * h_target) / (R * T_kelvin))




# I2C 통신 초기화
i2c = board.I2C()  # I2C 핀: SDA와 SCL
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# 선택적: 해수면 기압 설정 (기본값은 1013.25 hPa) -> standard value
bme280.sea_level_pressure = P0_new  #Jinju sea level pressure

print("BME280 Sensor Test")

while True:
    print(f"Temperature: {bme280.temperature:.1f} °C")
    print(f"Humidity: {bme280.humidity:.1f} %")
    print(f"Pressure: {bme280.pressure:.1f} hPa")
    print(f"Altitude: {bme280.altitude:.2f} m")
    print()
    time.sleep(1)  # 1초 간격으로 출력
