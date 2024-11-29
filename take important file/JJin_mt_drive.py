import RPi.GPIO as GPIO
from time import sleep

# GPIO 핀 설정
IN1 = 12
IN2 = 16
IN3 = 20
IN4 = 21

steps_per_revolution = 200  # NEMA17의 한 바퀴 스텝 수
steps_for_half_revolution = steps_per_revolution // 2

# 스텝핑 시퀀스 (하프 스텝)
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

def single_step(step_index):
    GPIO.output(IN1, step_sequence[step_index][0])
    GPIO.output(IN2, step_sequence[step_index][1])
    GPIO.output(IN3, step_sequence[step_index][2])
    GPIO.output(IN4, step_sequence[step_index][3])

def move_stepper(steps, direction):
    for _ in range(steps):
        for step_index in range(8):  # 하프 스텝 방식
            index = step_index if direction else 7 - step_index
            single_step(index)
            sleep(0.002)  # 스텝 간 딜레이

try:
    while True:
        # 정방향 반바퀴 회전
        move_stepper(steps_for_half_revolution, True)
        sleep(1)
        
        # 역방향 반바퀴 회전
        move_stepper(steps_for_half_revolution, False)
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
