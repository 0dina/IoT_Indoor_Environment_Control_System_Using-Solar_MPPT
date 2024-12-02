import time
import pymysql
from temp_class import BME280Sensor
from wind_class import WindDirectionSensor
from rain_class import RainSensor
from usb_serial_class import USBSerial
from wind_speed_class import WindSpeedSensor
from if_mt_control_class import AirQualityControlSystem  # AirQualityControlSystem 추가

# 데이터베이스 연결 함수
def sql_connect():
    return pymysql.connect(
        host='192.168.0.90',  # 호스트
        user='root',
        password='mypassword',  # 비밀번호
        db='dina',  # 데이터베이스 이름
        charset='utf8'
    )

# 중복 데이터 확인 함수
def is_duplicate(conn, data):
    cur = conn.cursor()
    sql = """
        SELECT COUNT(*) FROM choi
        WHERE Temperature = %s AND Humidity = %s AND Pressure = %s AND WindDirection = %s AND WindSpeed = %s AND Rainfall = %s AND Dust = %s AND WindowState = %s
    """
    cur.execute(sql, data)
    return cur.fetchone()[0] > 0

# 데이터 삽입 함수
def insert_data(conn, data):
    cur = conn.cursor()
    sql = """
        INSERT INTO choi (Temperature, Humidity, Pressure, WindDirection, WindSpeed, Rainfall, Dust, WindowState)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql, data)
    conn.commit()

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

    # 이전 데이터 저장 변수 (이상치 검출용)
    last_values = None

    try:
        # Open the USB serial port
        usb_serial.open()

        while True:
            # Wait for USB serial data
            usb_received_data = usb_serial.receive()

            # If USB data is received, read other sensor data
            if usb_received_data:
                # 센서 데이터 읽기
                temperature = round(bme280.read_temperature(), 2)
                humidity = round(bme280.read_humidity(), 2)
                pressure = round(bme280.read_pressure(), 2)
                wind_direction = wind_sensor.get_direction()
                wind_speed = round(wind_speed_sensor.measure_wind_speed(), 2)
                rainfall = round(rain_sensor.get_rainfall(), 2)

                # USB 데이터 읽기
                dust_data = usb_serial.receive()

                # USB 데이터가 없을 경우 처리
                if dust_data is None or not dust_data.isdigit():
                    continue

                # Convert dust data to integer
                dust = int(dust_data)

                # 데이터 유효성 검사
                if not (0 <= temperature <= 100):
                    continue
                if not (0 <= humidity <= 100):
                    continue
                if not (900 <= pressure <= 1100):  # Typical pressure range in hPa
                    continue
                if not (0 <= wind_speed <= 200):  # Typical wind speed range in km/h
                    continue
                if not (0 <= rainfall):
                    continue
                if not (-1000 <= dust <= 1000):  # Assuming a valid dust range (adjust if needed)
                    continue

                # 이상치 검출
                if last_values:
                    if abs(temperature - last_values[0]) > 20:
                        continue
                last_values = (temperature, humidity, pressure, wind_direction, wind_speed, rainfall, dust)

                # 창문 상태 추적
                window_state = air_quality_control_system.window_control.window_state

                # 데이터베이스 연결
                conn = sql_connect()

                # 중복 데이터 확인
                if is_duplicate(conn, (temperature, humidity, pressure, wind_direction, wind_speed, rainfall, dust, window_state)):
                    conn.close()
                    continue

                # 데이터 삽입
                print(f"Inserting data: ({temperature}, {humidity}, {pressure}, {wind_direction}, {wind_speed}, {rainfall}, {dust}, '{window_state}')")
                insert_data(conn, (temperature, humidity, pressure, wind_direction, wind_speed, rainfall, dust, window_state))

                conn.close()
                print("Connection closed")

                # Delay to prevent rapid polling
                time.sleep(1)

            except Exception as e:
                print(f"Error: {e}")
    finally:
        # Cleanup
        usb_serial.close()
        wind_speed_sensor.cleanup()

if __name__ == "__main__":
    main()
