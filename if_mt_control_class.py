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

class WindowControl:
    def __init__(self, steps_per_revolution, pin_setup):
        self.steps_per_revolution = steps_per_revolution
        self.pin_setup = pin_setup
        self.window_state = "open"
        
    def single_step(self, step_index):
        """단일 스텝 동작"""
        GPIO.output(IN1, step_sequence[step_index][0])
        GPIO.output(IN2, step_sequence[step_index][1])
        GPIO.output(IN3, step_sequence[step_index][2])
        GPIO.output(IN4, step_sequence[step_index][3])

    def move_stepper(self, steps, direction):
        """모터를 회전시키는 함수"""
        for _ in range(steps):
            for step_index in range(4):
                index = step_index if direction else 3 - step_index
                self.single_step(index)
                sleep(0.005)

    def open_window(self):
        """창문 열기"""
        print("Opening window...")
        self.move_stepper(self.steps_per_revolution, True)  # 정방향
        self.window_state = "open"

    def close_window(self):
        """창문 닫기"""
        print("Closing window...")
        self.move_stepper(self.steps_per_revolution, False)  # 역방향
        self.window_state = "closed"


class USBCommunication:
    def __init__(self, port, baudrate, timeout):
        self.usb_serial = USBSerial(port=port, baudrate=baudrate, timeout=timeout)

    def open_connection(self):
        """USB 포트 열기"""
        self.usb_serial.open()

    def close_connection(self):
        """USB 포트 닫기"""
        self.usb_serial.close()

    def receive_data(self):
        """USB 데이터 수신"""
        return self.usb_serial.receive()


class AirQualityControlSystem:
    def __init__(self, dust_threshold=5):
        self.dust_threshold = dust_threshold
        self.window_control = WindowControl(steps_per_revolution, [IN1, IN2, IN3, IN4])
        self.usb_comm = USBCommunication('/dev/ttyACM0', 9600, 1)

    def run(self):
        """시스템 실행"""
        self.usb_comm.open_connection()
        
        try:
            while True:
                usb
