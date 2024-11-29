import time
from temp_class import BME280Sensor
from wind_class import WindDirectionSensor
from rain_class import RainSensor

def main():
    # Initialize sensors
    bme280 = BME280Sensor(measured_pressure=1018.0, target_altitude=15.0, temperature_celsius=25.0)
    wind_sensor = WindDirectionSensor()
    rain_sensor = RainSensor(pin=6)

    try:
        while True:
            # Read temperature, humidity, pressure, and altitude from BME280
            bme280.print_readings()

            # Read wind direction voltage
            wind_sensor.print_wind_direction()

            # Read rainfall over the last minute
            rainfall = rain_sensor.get_rainfall()
            print(f"Rainfall Detected: {rainfall:.2f}mm")

            print("\n---")
            time.sleep(1)  # Adjust the delay as needed
    except KeyboardInterrupt:
        print("Stopping all sensors...")
    finally:
        rain_sensor.cleanup()  # Clean up GPIO resources for rain sensor

if __name__ == "__main__":
    main()