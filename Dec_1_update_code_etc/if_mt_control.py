import RPi.GPIO as GPIO
from time import sleep
from usb_serial_class import USBSerial  # USBSerial 클래스 가져오기

# GPIO 핀 설정 (HW-095 IN1~IN4에 연결된 핀)
IN1 = 12
IN2 = 16
IN3 = 20
IN4 = 21

# 스텝 모터 설정
steps_per_revolution = 82  # 창문 길이에 맞게 설정된 값
step_sequence = [
    [1, 0, 1, 0],  # 스텝 1
    [0, 1, 1, 0],  # 스텝 2
    [0, 1, 0, 1],  # 스텝 3
    [1, 0, 0, 1],  # 스텝 4
]

# GPIO 설정
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
        for step_index in range(4):
            index = step_index if direction else 3 - step_index
            single_step(index)
            sleep(0.005)

def main():
    # USB Serial 초기화
    usb_serial = USBSerial(port='/dev/ttyACM0', baudrate=9600, timeout=1)

    try:
        # USB 포트 열기
        usb_serial.open()

        window_state = "open"  # 초기 창문 상태
        dust_threshold = 5  # 미세먼지 임계값 설정

        while True:
            # USB 데이터 수신
            usb_received_data = usb_serial.receive()

            if usb_received_data:
                try:
                    # 숫자로만 들어온 경우 처리
                    if usb_received_data.isdigit():
                        dust_sensor = int(usb_received_data)
                    else:  # JSON 형식으로 들어온 경우 처리
                        dust_data = eval(usb_received_data)  # 예: {"dust_sensor": 10}
                        dust_sensor = dust_data.get("dust_sensor", 0)
                except Exception:
                    # 유효하지 않은 데이터는 무시하고 넘어감
                    continue

                print(f"Dust Sensor: {dust_sensor}")

                # 창문 상태 제어
                if dust_sensor > dust_threshold and window_state == "closed":
                    print("Air quality poor, opening window...")
                    move_stepper(steps_per_revolution, True)  # 정방향 (열기)
                    window_state = "open"

                # 역방향 동작 주석 처리
                elif dust_sensor <= dust_threshold and window_state == "open":
                    print("Air quality normal, closing window...")
                    move_stepper(steps_per_revolution, False)  # 역방향 (닫기)
                    window_state = "closed"

            sleep(1)  # 1초 대기
    except KeyboardInterrupt:
        print("Stopping program...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 리소스 정리
        usb_serial.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
