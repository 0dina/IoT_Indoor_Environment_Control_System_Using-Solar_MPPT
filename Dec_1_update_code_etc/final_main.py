import time
from temp_class import BME280Sensor
from wind_class import WindDirectionSensor
from rain_class import RainSensor
from usb_serial_class import USBSerial  # USBSerial 클래스 가져오기
from wind_speed_class import WindSpeedSensor  # WindSpeedSensor 클래스 가져오기
from if_mt_control_class import AirQualityControlSystem  # AirQualityControlSystem 클래스 불러오기

def main():
    # Initialize sensors
    bme280 = BME280Sensor(measured_pressure=1018.0, target_altitude=15.0, temperature_celsius=25.0)
    wind_sensor = WindDirectionSensor(json_file_path="wind_direction.json")
    rain_sensor = RainSensor(pin=6)
    wind_speed_sensor = WindSpeedSensor(wind_pin=17, radius_cm=9.0, adjustment=2.0, wind_interval=5)  # WindSpeedSensor 초기화

    # Initialize USB Serial
    usb_serial = USBSerial(port='/dev/ttyACM0', baudrate=9600, timeout=1)

    # Initialize AirQualityControlSystem for window control
    air_quality_control_system = AirQualityControlSystem(dust_threshold=5)  # 미세먼지 임계값 설정

    try:
        # Open the USB serial port
        usb_serial.open()

        while True:
            # Wait for USB serial data
            usb_received_data = usb_serial.receive()

            # If USB data is received, read other sensor data
            if usb_received_data:
                # Read sensor data
                temperature = bme280.read_temperature()
                humidity = bme280.read_humidity()
                pressure = bme280.read_pressure()
                altitude = bme280.read_altitude()
                wind_direction = wind_sensor.get_direction()
                rainfall = rain_sensor.get_rainfall()
                wind_speed = wind_speed_sensor.measure_wind_speed()  # 풍속 측정

                # Print all sensor data together
                print(f"Temperature: {temperature:.1f} °C")
                print(f"Humidity: {humidity:.1f} %")
                print(f"Pressure: {pressure:.1f} hPa")
                print(f"Altitude: {altitude:.2f} m")
                print(f"Wind Direction: {wind_direction}")
                print(f"Wind Speed: {wind_speed:.2f} km/h")  # 풍속 출력
                print(f"Rainfall Detected: {rainfall:.2f} mm")
                print(f"Dust sensor Received: {usb_received_data}\n")

                # Air quality control (window open/close logic)
                air_quality_control_system.run()  # 미세먼지 농도에 따라 창문 제어

            time.sleep(1)  # 1초 대기

    except KeyboardInterrupt:
        print("Stopping all sensors...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        usb_serial.close()
        rain_sensor.cleanup()
        wind_speed_sensor.cleanup()

if __name__ == "__main__":
    main()
