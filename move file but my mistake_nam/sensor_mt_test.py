import RPi.GPIO as GPIO
from time import sleep

# GPIO 핀 설정 (HW-095 IN1~IN4에 연결된 핀)
IN1 = 12
IN2 = 16
IN3 = 20
IN4 = 21

steps_per_revolution = 200  # NEMA17의 한 바퀴 스텝 수
steps_for_half_revolution = steps_per_revolution // 2

# 스텝핑 시퀀스 (풀 스텝 방식)
step_sequence = [
    [1, 0, 1, 0],  # 스텝 1
    [0, 1, 1, 0],  # 스텝 2
    [0, 1, 0, 1],  # 스텝 3
    [1, 0, 0, 1],  # 스텝 4
]

# 창문 상태
window_open = False  # 창문 상태 (True: 열림, False: 닫힘)

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# 스텝 모터 단일 스텝
def single_step(step_index):
    GPIO.output(IN1, step_sequence[step_index][0])
    GPIO.output(IN2, step_sequence[step_index][1])
    GPIO.output(IN3, step_sequence[step_index][2])
    GPIO.output(IN4, step_sequence[step_index][3])

# 스텝 모터 움직임
def move_stepper(steps, direction):
    for _ in range(steps):
        for step_index in range(4):
            index = step_index if direction else 3 - step_index
            single_step(index)
            sleep(0.005)

# 창문 제어 함수
def control_window(pm_value, rainfall, wind_speed):
    global window_open

    # 창문 열기 조건
    if not window_open:
        if pm_value <= 100 and rainfall <= 10 and wind_speed <= 30:
            print("Opening window...")
            move_stepper(steps_for_half_revolution, True)
            window_open = True

    # 창문 닫기 조건
    elif window_open:
        if pm_value > 100 or rainfall > 10 or wind_speed > 30:
            print("Closing window...")
            move_stepper(steps_for_half_revolution, False)
            window_open = False

try:
    while True:
        # 센서 값 입력 (테스트 환경에서는 임의 값 사용)
        pm_value = int(input("Enter PM2.5 value: "))  # 미세먼지 값 입력
        rainfall = float(input("Enter rainfall (mm/h): "))  # 강우량 입력
        wind_speed = float(input("Enter wind speed (km/h): "))  # 풍속 입력

        # 창문 제어 로직
        control_window(pm_value, rainfall, wind_speed)

        sleep(1)  # 1초 대기 후 다시 체크

except KeyboardInterrupt:
    GPIO.cleanup()

finally:
    GPIO.cleanup()