from flask import Flask, render_template, jsonify, request
import pymysql

app = Flask(__name__)

# 데이터베이스 연결 설정
def get_db_connection():
    return pymysql.connect(
        host="192.168.0.90",
        user="root",
        password="mypassword",
        db="dina",
        charset="utf8"
    )

# 센서 데이터 가져오기
@app.route("/data", methods=["GET"])
def get_sensor_data():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM choi ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()
    connection.close()

    if data:
        keys = ["temperature", "humidity", "pressure", "wind_direction", "wind_speed", "rainfall", "dust"]
        return jsonify(dict(zip(keys, data[1:])))
    return jsonify({"error": "No data available"})

# 창문 상태 업데이트
@app.route("/window", methods=["POST"])
def control_window():
    action = request.json.get("action")
    status = "open" if action == "open" else "closed"
    # 실제 GPIO 핀 제어 로직 추가 (예: Raspberry Pi 모터 컨트롤)
    return jsonify({"status": status})

# 메인 페이지
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
