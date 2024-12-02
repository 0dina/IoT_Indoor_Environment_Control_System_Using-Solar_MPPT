from flask import Flask, render_template, jsonify
from db import sql_connect, get_all_sensor_data  # get_all_sensor_data 추가
from time import sleep

app = Flask(__name__)

# 전역 변수로 창문 상태 관리
window_state = "closed"

@app.route('/')
def index():
    # 데이터베이스에서 센서 데이터 가져오기
    conn = sql_connect()
    sensor_data = get_all_sensor_data(conn)  # DB에서 센서 데이터 가져오기
    conn.close()

    # 데이터를 딕셔너리로 변환하여 웹에 전달
    data = {
        "temperature": sensor_data[0],  # 온도
        "humidity": sensor_data[1],     # 습도
        "pressure": sensor_data[2],     # 압력
        "wind_direction": sensor_data[3],  # 풍향
        "wind_speed": sensor_data[4],   # 풍속
        "rainfall": sensor_data[5],     # 강수량
        "dust": sensor_data[6],         # 미세먼지
        "window_state": sensor_data[7]  # 창문 상태
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
    
    # 데이터베이스에 상태 저장
    conn = sql_connect()
    insert_data(conn, (22.87, 51.82, 1015.47, 'ESE', 0.0, 0.0, 8, window_state))  # 예시 데이터 삽입
    conn.close()
    
    return jsonify({"status": "success", "message": f"Window is now {window_state}."})

@app.route('/api/data', methods=['GET'])
def get_sensor_data():
    # DB에서 센서 데이터를 가져오는 로직
    conn = sql_connect()
    sensor_data = get_all_sensor_data(conn)
    conn.close()

    data = {
        "temperature": sensor_data[0],
        "humidity": sensor_data[1],
        "pressure": sensor_data[2],
        "wind_direction": sensor_data[3],
        "wind_speed": sensor_data[4],
        "rainfall": sensor_data[5],
        "dust": sensor_data[6],
        "window_state": sensor_data[7]
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
