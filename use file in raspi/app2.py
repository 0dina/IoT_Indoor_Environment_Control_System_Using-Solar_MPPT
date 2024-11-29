from flask import Flask, jsonify, request
import pymysql
from temp_class import BME280Sensor
from wind_class import WindDirectionSensor
from rain_class import RainSensor
import time

app = Flask(__name__)

# MariaDB 연결 함수
def sql_connect():
    return pymysql.connect(
        host='192.168.0.90',  # 데이터베이스 호스트
        user='root',          # 사용자 이름
        password='mypassword',  # 비밀번호
        db='dina',            # 데이터베이스 이름
        charset='utf8'
    )

# 중복 데이터 확인 함수
def is_duplicate(conn, data):
    cur = conn.cursor()
    sql = """
        SELECT COUNT(*) FROM choi
        WHERE Temperature = %s AND Humidity = %s AND Pressure = %s AND WindVoltage = %s AND Rainfall = %s
    """
    cur.execute(sql, data)
    return cur.fetchone()[0] > 0

# 데이터 삽입 함수
def insert_data(conn, data):
    cur = conn.cursor()
    sql = """
        INSERT INTO choi (Temperature, Humidity, Pressure, WindVoltage, Rainfall)
        VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(sql, data)
    conn.commit()

# 센서 초기화
bme280 = BME280Sensor(measured_pressure=1018.0, target_altitude=15.0, temperature_celsius=25.0)
wind_sensor = WindDirectionSensor()
rain_sensor = RainSensor(pin=6)

# 실시간 센서값 저장용 전역 변수
current_sensor_data = {}

@app.route('/api/sensors', methods=['GET'])
def get_sensor_data():
    """실시간 센서 데이터를 반환"""
    return jsonify(current_sensor_data)

@app.route('/api/history', methods=['GET'])
def get_sensor_history():
    """데이터베이스에서 센서 데이터 반환"""
    conn = sql_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM choi ORDER BY id DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

def update_sensor_data():
    """센서 데이터를 읽고 데이터베이스에 저장"""
    global current_sensor_data
    last_values = None

    while True:
        try:
            # 센서 데이터 읽기
            temperature = round(bme280.read_temperature(), 2)
            humidity = round(bme280.read_humidity(), 2)
            pressure = round(bme280.read_pressure(), 2)
            wind_voltage = round(wind_sensor.read_wind_direction(), 2)
            rainfall = round(rain_sensor.get_rainfall(), 2)

            # 데이터 유효성 검사
            if not (0 <= temperature <= 100): continue
            if not (0 <= humidity <= 100): continue
            if not (900 <= pressure <= 1100): continue
            if not (0 <= wind_voltage <= 5): continue
            if not (0 <= rainfall): continue

            # 이상치 검사
            if last_values and abs(temperature - last_values[0]) > 20:
                continue
            last_values = (temperature, humidity, pressure, wind_voltage, rainfall)

            # 실시간 데이터 저장
            current_sensor_data = {
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure,
                "wind_voltage": wind_voltage,
                "rainfall": rainfall,
            }

            # 데이터베이스 연결
            conn = sql_connect()

            # 중복 데이터 확인 및 삽입
            if not is_duplicate(conn, last_values):
                insert_data(conn, last_values)
                print(f"Data inserted: {last_values}")
            else:
                print("Duplicate data, skipping insertion")

            conn.close()
            time.sleep(1)
        except Exception as e:
            print(f"Error in sensor data processing: {e}")

# 백그라운드에서 센서 데이터를 지속적으로 업데이트
import threading
sensor_thread = threading.Thread(target=update_sensor_data, daemon=True)
sensor_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
