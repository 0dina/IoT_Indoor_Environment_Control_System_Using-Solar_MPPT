import RPi.GPIO as GPIO
import time
import math

class WindSpeedSensor:
    def __init__(self, wind_pin=17, radius_cm=9.0, adjustment=2.0, wind_interval=5):
        # GPIO 핀 및 설정값 초기화
        self.wind_pin = wind_pin
        self.radius_cm = radius_cm
        self.adjustment = adjustment
        self.wind_interval = wind_interval

        # 계산 상수
        self.CM_IN_A_KM = 100000.0
        self.SECS_IN_AN_HOUR = 3600

        # 회전 수 초기화
        self.wind_count = 0

        # GPIO 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.wind_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.wind_pin, GPIO.FALLING, callback=self._spin, bouncetime=200)

    def _spin(self, channel):
        """GPIO 핀에서 신호를 감지할 때 호출되는 내부 함수."""
        self.wind_count += 1

    def calculate_speed(self):
        """현재 측정된 회전 수를 바탕으로 풍속을 계산."""
        if self.wind_count == 0 or self.wind_count > 1000:
            return 0.0
        circumference_cm = (2 * math.pi) * self.radius_cm
        rotations = self.wind_count / 2.0
        dist_km = (circumference_cm * rotations) / self.CM_IN_A_KM
        km_per_sec = dist_km / self.wind_interval
        km_per_hour = km_per_sec * self.SECS_IN_AN_HOUR
        final_speed = km_per_hour * self.adjustment
        return final_speed

    def reset_wind_count(self):
        """회전 수 초기화."""
        self.wind_count = 0

    def measure_wind_speed(self):
        """
        wind_interval 동안 회전 수를 측정하고 풍속을 계산.
        Returns:
            float: 계산된 풍속 (km/h)
        """
        start_time = time.time()
        end_time = start_time + self.wind_interval
        self.reset_wind_count()

        while time.time() <= end_time:
            time.sleep(0.1)

        return self.calculate_speed()

    def cleanup(self):
        """GPIO 리소스 정리."""
        GPIO.cleanup()
