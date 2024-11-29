from flask import Flask, jsonify, request, render_template
import pymysql
from temp_class import BME280Sensor
from wind_class import WindDirectionSensor
from rain_class import RainSensor

app = Flask(__name__)

# 데이터베이스 연결 함수
def sql_connect():
    return pymysql.connect(
        host='192.168.0.90',
        user='root',
        password='mypassword',
        db='dina',
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

# 센서 데이터 읽기 함수
def read_sensors():
    bme280 = BME280Sensor(measured_pressure=1018.0, target_altitude=15.0, temperature_celsius=25.0)
    wind_sensor = WindDirectionSensor()
    rain_sensor = RainSensor(pin=6)

    return {
        "temperature": round(bme280.read_temperature(), 2),
        "humidity": round(bme280.read_humidity(), 2),
        "pressure": round(bme280.read_pressure(), 2),
        "wind_voltage": round(wind_sensor.read_wind_direction(), 2),
        "rainfall": round(rain_sensor.get_rainfall(), 2),
    }

# Flask Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/sensors", methods=["GET"])
def get_sensors():
    """실시간 센서 데이터를 반환하고 데이터베이스에 저장"""
    conn = sql_connect()
    try:
        sensor_data = read_sensors()

        # 데이터 유효성 검사
        if not (0 <= sensor_data["temperature"] <= 100):
            return jsonify({"error": "Invalid temperature value"}), 400
        if not (0 <= sensor_data["humidity"] <= 100):
            return jsonify({"error": "Invalid humidity value"}), 400
        if not (900 <= sensor_data["pressure"] <= 1100):
            return jsonify({"error": "Invalid pressure value"}), 400
        if not (0 <= sensor_data["wind_voltage"] <= 5):
            return jsonify({"error": "Invalid wind voltage value"}), 400
        if sensor_data["rainfall"] < 0:
            return jsonify({"error": "Invalid rainfall value"}), 400

        # 중복 데이터 확인
        if is_duplicate(conn, (
            sensor_data["temperature"],
            sensor_data["humidity"],
            sensor_data["pressure"],
            sensor_data["wind_voltage"],
            sensor_data["rainfall"]
        )):
            return jsonify({"status": "Duplicate data, skipped insertion"}), 200

        # 데이터 삽입
        insert_data(conn, (
            sensor_data["temperature"],
            sensor_data["humidity"],
            sensor_data["pressure"],
            sensor_data["wind_voltage"],
            sensor_data["rainfall"]
        ))

        return jsonify(sensor_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/history", methods=["GET"])
def get_history():
    """과거 데이터를 반환"""
    conn = sql_connect()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM choi ORDER BY id DESC LIMIT 100")
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
