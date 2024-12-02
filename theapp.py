from flask import Flask, render_template, jsonify, request
from if_mt_control_class import AirQualityControlSystem
from db import sql_connect, insert_data
from time import sleep

app = Flask(__name__)

# 전역 변수로 창문 상태 관리
window_state = "closed"

# Air Quality Control System 초기화
air_quality_system = AirQualityControlSystem(dust_threshold=5)

@app.route('/')
def index():
    # 웹에서 보여줄 현재 센서 상태 가져오기
    data = {
        "temperature": 22.87,  # 예시 데이터 (이 부분은 실제 데이터로 바꿔주세요)
        "humidity": 51.82,
        "pressure": 1015.47,
        "wind_direction": "ESE",
        "wind_speed": 0.0,
        "rainfall": 0.0,
        "dust": 8,
        "window_state": window_state  # 현재 창문 상태 표시
    }
    return render_template('index.html', data=data)

@app.route('/update', methods=['POST'])
def update_window_state():
    global window_state
    # 사용자가 창문을 열거나 닫을 때 처리
    action = request.form.get('action')
    
    if action == 'open' and window_state == 'closed':
        # 창문 열기
        air_quality_system.window_control.open_window()
        window_state = "open"
    elif action == 'close' and window_state == 'open':
        # 창문 닫기
        air_quality_system.window_control.close_window()
        window_state = "closed"
    else:
        return jsonify({"status": "error", "message": f"Window is already {window_state}."})
    
    # 데이터베이스에 상태 저장 (여기서는 예시로 임시 데이터만 사용)
    conn = sql_connect()
    insert_data(conn, (22.87, 51.82, 1015.47, 'ESE', 0.0, 0.0, 8, window_state))  # 삽입 예시
    conn.close()
    
    return jsonify({"status": "success", "message": f"Window is now {window_state}."})

@app.route('/api/data', methods=['GET'])
def get_sensor_data():
    # 여기서 실제 센서 데이터를 가져오는 로직을 작성합니다.
    # 예시 데이터 반환
    data = {
        "temperature": 22.87,
        "humidity": 51.82,
        "pressure": 1015.47,
        "wind_direction": "ESE",
        "wind_speed": 0.0,
        "rainfall": 0.0,
        "dust": 8,
        "window_state": window_state
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
