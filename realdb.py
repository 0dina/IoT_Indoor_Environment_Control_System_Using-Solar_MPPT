import pymysql

# 데이터베이스 연결 함수
def sql_connect():
    return pymysql.connect(
        host='192.168.0.90',  # 호스트 주소
        user='root',
        password='mypassword',  # 데이터베이스 비밀번호
        db='dina',  # 데이터베이스 이름
        charset='utf8'
    )

# 가장 최근의 데이터 가져오기
def get_latest_sensor_data():
    conn = sql_connect()
    cur = conn.cursor()

    # 가장 최근의 데이터를 가져오는 SQL 쿼리
    sql = "SELECT * FROM choi ORDER BY Time DESC LIMIT 1"
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()

    if result:
        # 데이터가 있으면 각 센서 값 반환
        return {
            "temperature": result[0],
            "humidity": result[1],
            "pressure": result[2],
            "wind_direction": result[3],
            "wind_speed": result[4],
            "rainfall": result[5],
            "dust": result[6],
            "window_state": result[7]  # 창문 상태 추가
        }
    else:
        # 데이터가 없으면 기본 값 반환
        return None

# 각 센서의 개별 데이터를 가져오는 함수들

def get_temperature():
    conn = sql_connect()
    cur = conn.cursor()
    sql = "SELECT Temperature FROM choi ORDER BY Time DESC LIMIT 1"
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_humidity():
    conn = sql_connect()
    cur = conn.cursor()
    sql = "SELECT Humidity FROM choi ORDER BY Time DESC LIMIT 1"
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_pressure():
    conn = sql_connect()
    cur = conn.cursor()
    sql = "SELECT Pressure FROM choi ORDER BY Time DESC LIMIT 1"
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_wind_direction():
    conn = sql_connect()
    cur = conn.cursor()
    sql = "SELECT WindDirection FROM choi ORDER BY Time DESC LIMIT 1"
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_wind_speed():
    conn = sql_connect()
    cur = conn.cursor()
    sql = "SELECT WindSpeed FROM choi ORDER BY Time DESC LIMIT 1"
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_rainfall():
    conn = sql_connect()
    cur = conn.cursor()
    sql = "SELECT Rainfall FROM choi ORDER BY Time DESC LIMIT 1"
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_dust():
    conn = sql_connect()
    cur = conn.cursor()
    sql = "SELECT Dust FROM choi ORDER BY Time DESC LIMIT 1"
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_window_state():
    conn = sql_connect()
    cur = conn.cursor()
    sql = "SELECT WindowState FROM choi ORDER BY Time DESC LIMIT 1"
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None
