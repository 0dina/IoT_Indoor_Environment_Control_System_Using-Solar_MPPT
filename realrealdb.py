import pymysql
from time import sleep

# 데이터베이스 연결 함수
def sql_connect():
    return pymysql.connect(
        host='192.168.0.90',  # 실제 MariaDB 또는 MySQL 호스트 주소
        user='root',
        password='mypassword',  # 실제 비밀번호
        db='dina',  # 실제 데이터베이스 이름
        charset='utf8mb4'
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

# 특정 데이터 가져오기 함수 (최신 데이터)
def get_latest_data(conn):
    cur = conn.cursor()
    sql = "SELECT * FROM choi ORDER BY time DESC LIMIT 1"
    cur.execute(sql)
    return cur.fetchone()  # 가장 최신 데이터 한 행을 반환
