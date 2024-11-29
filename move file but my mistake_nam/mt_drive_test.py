import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
IN1 = 12
IN2 = 16
IN3 = 20
IN4 = 21
ENA = 18
ENB = 19

# 8단계 스테핑 모터의 시퀀스
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)


# PWM 초기화
pwm_ena = GPIO.PWM(ENA, 50)  # 100Hz
pwm_enb = GPIO.PWM(ENB, 50)  # 100Hz
pwm_ena.start(100)  # 100% 듀티 사이클
pwm_enb.start(100)  # 100% 듀티 사이클


def set_motor_pins(state):
    """스테핑 모터의 IN1~IN4 핀 상태 설정"""
    GPIO.output(IN1, state[0])
    GPIO.output(IN2, state[1])
    GPIO.output(IN3, state[2])
    GPIO.output(IN4, state[3])


def rotate_motor(direction, steps=50):
    """모터 회전: direction=1(정방향), direction=-1(역방향), steps=회전 스텝 수"""
    if direction == 1:  # 정방향
        sequence = step_sequence
    else:  # 역방향
        sequence = list(reversed(step_sequence))

    for _ in range(steps):
        for step in sequence:
            set_motor_pins(step)
            time.sleep(0.02)  # 속도 조절 (20ms)


if __name__ == "__main__":
    try:
        while True:
            print("forward")
            rotate_motor(1, steps=50)  # 정방향 100스텝 (반바퀴)
            time.sleep(1)  # 1초 대기

            print("reverse")
            rotate_motor(-1, steps=50)  # 역방향 100스텝 (반바퀴)
            time.sleep(1)  # 1초 대기
    except KeyboardInterrupt:
        print("프로그램 종료")
    finally:
        pwm_ena.stop()
        pwm_enb.stop()
        GPIO.cleanup()