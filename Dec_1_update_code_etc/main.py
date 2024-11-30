import time
from temp_class import BME280Sensor
from wind_class import WindDirectionSensor
from rain_class import RainSensor
from usb_serial_class import USBSerial  # USBSerial 클래스 가져오기

def main():
    # Initialize sensors
    bme280 = BME280Sensor(measured_pressure=1018.0, target_altitude=15.0, temperature_celsius=25.0)
    wind_sensor = WindDirectionSensor()
    rain_sensor = RainSensor(pin=6)

    # Initialize USB Serial
    usb_serial = USBSerial(port='/dev/ttyACM0', baudrate=9600, timeout=1)

    try:
        # Open the USB serial port
        usb_serial.open()

        while True:
            # Wait for USB serial data
            
            usb_received_data = usb_serial.receive()

            # If USB data is received, read other sensor data
            if usb_received_data:
                temperature = bme280.read_temperature()
                humidity = bme280.read_humidity()
                pressure = bme280.read_pressure()
                altitude = bme280.read_altitude()
                wind_voltage = wind_sensor.read_wind_direction()
                rainfall = rain_sensor.get_rainfall()

                # Print all data together
                print(f"Temperature: {temperature:.1f} °C")
                print(f"Humidity: {humidity:.1f} %")
                print(f"Pressure: {pressure:.1f} hPa")
                print(f"Altitude: {altitude:.2f} m")
                print(f"Wind Voltage: {wind_voltage:.2f} V")
                print(f"Rainfall Detected: {rainfall:.2f} mm")
                print(f"Dust sensor Received: {usb_received_data}\n")
           
            
            
            time.sleep(1)  # Adjust the delay as needed
    except KeyboardInterrupt:
        print("Stopping all sensors...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        usb_serial.close()  # Close USB serial port
        rain_sensor.cleanup()  # Clean up GPIO resources for rain sensor

if __name__ == "__main__":
    main()
