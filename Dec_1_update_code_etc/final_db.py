import time
import pymysql
from temp_class import BME280Sensor
from wind_class import WindDirectionSensor
from rain_class import RainSensor
from usb_serial_class import USBSerial  # USBSerial 클래스 가져오기
from wind_speed_class import WindSpeedSensor  # WindSpeedSensor 클래스 가져오기
from if_mt_control_class import MotorController  # MotorController 클래스 불러오기

# 데이터베이스 연결 함수
def sql_connect():
    return pymysql.connect(
        host='192.168.0.90',  # 새로운 호스트
        user='root',
        password='mypassword',  # 새로운 비밀번호
        db='dina',  # 새로운 데이터베이스 이름
        charset='utf8'
    )

# 중복 데이터 확인 함수
def is_duplicate(conn, data):
    cur = conn.cursor()
    sql = """
        SELECT COUNT(*) FROM choi
        WHERE Temperature = %s AND Humidity = %s AND Pressure = %s AND WindDirection = %s AND WindSpeed = %s AND Rainfall = %s AND Dust = %s
    """
    cur.execute(sql, data)
    return cur.fetchone()[0] > 0

# 데이터 삽입 함수
def insert_data(conn, data):
    cur = conn.cursor()
    sql = """
        INSERT INTO choi (Temperature, Humidity, Pressure, WindDirection, WindSpeed, Rainfall, Dust)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql, data)
    conn.commit()

# 창문 상태 업데이트 함수
def update_window_status(conn, state):
    cur = conn.cursor()
    cur.execute("INSERT INTO window_status (state) VALUES (%s)", (state,))
    conn.commit()

def main():
    # Initialize sensors
    bme280 = BME280Sensor(measured_pressure=1018.0, target_altitude=15.0, temperature_celsius=25.0)
    wind_sensor = WindDirectionSensor(json_file_path="wind_direction.json")
    rain_sensor = RainSensor(pin=6)
    wind_speed_sensor = WindSpeedSensor(wind_pin=17, radius_cm=9.0, adjustment=2.0, wind_interval=5)  # WindSpeedSensor 초기화

    # Initialize USB Serial
    usb_serial = USBSerial(port='/dev/ttyACM0', baudrate=9600, timeout=1)

    # Initialize MotorController for window control
    motor_controller = MotorController(steps_per_revolution=82, pins=[12, 16, 20, 21])  # 스텝 모터 핀 설정

    window_state = "closed"  # 초기 창문 상태
    dust_threshold = 5  # 미세먼지 임계값 설정

    try:
        # Open the USB serial port
        usb_serial.open()

        while True:
            # Wait for USB serial data
            usb_received_data = usb_serial.receive()

            # If USB data is received, read other sensor data
            if usb_received_data:
                try:
                    # 숫자로만 들어온 경우 처리
                    if usb_received_data.isdigit():
                        dust_sensor = int(usb_received_data)
                    else:  # JSON 형식으로 들어온 경우 처리
                        dust_data = eval(usb_received_data)  # 예: {"dust_sensor": 10}
                        dust_sensor = dust_data.get("dust_sensor", 0)
                except Exception:
                    # 유효하지 않은 데이터는 무시하고 넘어감
                    continue

                print(f"Dust Sensor: {dust_sensor}")

                # 창문 상태 제어
                if dust_sensor > dust_threshold and window_state == "closed":
                    print("Air quality poor, opening window...")
                    motor_controller.open_window()
                    window_state = "open"
                    # 데이터베이스에 창문 상태 업데이트
                    conn = sql_connect()
                    update_window_status(conn, window_state)
                    conn.close()

                elif dust_sensor <= dust_threshold and window_state == "open":
                    print("Air quality normal, closing window...")
                    motor_controller.close_window()
                    window_state = "closed"
                    # 데이터베이스에 창문 상태 업데이트
                    conn = sql_connect()
                    update_window_status(conn, window_state)
                    conn.close()

                # 센서 데이터 기록
                conn = sql_connect()
                insert_data(conn, (bme280.read_temperature(), bme280.read_humidity(), bme280.read_pressure(),
                                   wind_sensor.get_direction(), wind_speed_sensor.measure_wind_speed(),
                                   rain_sensor.get_rainfall(), dust_sensor))
                conn.close()

            time.sleep(1)  # 1초 대기

    except KeyboardInterrupt:
        print("Stopping program...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        usb_serial.close()
        motor_controller.cleanup()
        rain_sensor.cleanup()
        wind_speed_sensor.cleanup()

if __name__ == "__main__":
    main()
