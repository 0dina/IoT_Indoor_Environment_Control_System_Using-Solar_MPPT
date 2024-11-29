from flask import Flask, jsonify, request
import pymysql
from temp_class import BME280Sensor
from wind_class import WindDirectionSensor
from rain_class import RainSensor
from JJin_mt_drive import MotorDriver
import time

app = Flask(__name__)

# MariaDB 연결 함수
def sql_connect():
    return pymysql.connect(
        host='192.168.0.90',
        user='root',
        password='mypassword',  # 데이터베이스 비밀번호
        db='dina',             # 데이터베이스 이름
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

# 데이터베이스에서 창문 상태 저장 함수
def save_window_status(state):
    conn = sql_connect()
    cursor = conn.cursor()
    sql = "INSERT INTO window_status (state) VALUES (%s)"
    cursor.execute(sql, (state,))
    conn.commit()
    cursor.close()
    conn.close()

# 창문 상태 조회 함수
def get_latest_window_status():
    conn = sql_connect()
    cursor = conn.cursor()
    sql = "SELECT state FROM window_status ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "closed"

# 창문 제어용 모터 초기화
motor = MotorDriver()

# 창문 상태 변수
window_status = {"state": get_latest_window_status()}  # 데이터베이스에서 초기 상태 로드

@app.route("/api/window", methods=["GET", "POST"])
def control_window():
    if request.method == "GET":
        """창문 상태를 반환"""
        return jsonify(window_status)

    if request.method == "POST":
        """창문 상태를 제어"""
        action = request.json.get("action")
        if action not in ["open", "close"]:
            return jsonify({"error": "Invalid action"}), 400

        if window_status["state"] == action:
            return jsonify({"error": f"창문이 이미 {action} 상태입니다."}), 400

        # 창문 제어
        try:
            if action == "open":
                motor.open_window()  # 창문 열기
            elif action == "close":
                motor.close_window()  # 창문 닫기
            window_status["state"] = action
            save_window_status(action)  # 상태 저장
            return jsonify({"status": f"창문이 {action}되었습니다."})
        except Exception as e:
            return jsonify({"error": f"창문 제어 실패: {str(e)}"}), 500

# 센서 초기화
bme280 = BME280Sensor(measured_pressure=1018.0, target_altitude=15.0, temperature_celsius=25.0)
wind_sensor = WindDirectionSensor()
rain_sensor = RainSensor(pin=6)

# 실시간 센서 데이터 저장용 전역 변수
current_sensor_data = {}

@app.route("/api/sensors", methods=["GET"])
def get_sensor_data():
    """실시간 센서 데이터를 반환"""
    return jsonify(current_sensor_data)

@app.route("/api/history", methods=["GET"])
def get_sensor_history():
    """choi 테이블에서 과거 데이터 반환"""
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
            if not is_duplicate(conn, list(current_sensor_data.values())):
                insert_data(conn, list(current_sensor_data.values()))
                print(f"Data inserted: {current_sensor_data}")
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
