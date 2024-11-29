from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Simulated sensor data
sensor_data = {
    "wind_direction": 180,  # degrees
    "wind_speed": 5.0,      # m/s
    "rainfall": 0.0,        # mm
    "pm2_5": 35,            # µg/m³
    "temperature": 25.0,    # °C
    "humidity": 60.0        # %
}

window_status = {"state": "closed"}  # 창문 상태: "open" 또는 "closed"

def auto_control_logic():
    """자동 제어 로직"""
    if (
        sensor_data["pm2_5"] <= 100
        and sensor_data["rainfall"] <= 10
        and sensor_data["wind_speed"] <= 30
    ):
        return "open"
    return "closed"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/sensors", methods=["GET"])
def get_sensors():
    return jsonify(sensor_data)

@app.route("/api/window", methods=["GET", "POST"])
def control_window():
    if request.method == "GET":
        return jsonify(window_status)

    if request.method == "POST":
        action = request.json.get("action")
        if action == "auto":
            # 자동 제어 로직 실행
            auto_state = auto_control_logic()
            if window_status["state"] != auto_state:
                window_status["state"] = auto_state
                return jsonify({"status": f"창문이 자동으로 {auto_state}되었습니다."})
            return jsonify({"status": f"창문이 이미 {auto_state} 상태입니다."})
        elif action in ["open", "close"]:
            if window_status["state"] == action:
                return jsonify({"error": f"창문이 이미 {action} 상태입니다."}), 400
            window_status["state"] = action
            return jsonify({"status": f"창문이 {action}되었습니다."})
        return jsonify({"error": "잘못된 요청입니다."}), 400

if __name__ == "__main__":
    app.run(debug=True)
