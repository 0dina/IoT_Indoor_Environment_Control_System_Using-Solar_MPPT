import RPi.GPIO as GPIO
import time

RAIN_PIN = 6
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setup(RAIN_PIN,GPIO.IN,pull_up_down = GPIO.PUD_UP)

rain_count=0
RAIN_MM_PER_TIP = 0.2794

def rain_callback(channel):
    global rain_count
    rain_count+=1


try:
    GPIO.add_event_detect(RAIN_PIN,GPIO.FALLING, callback=rain_callback)
except RuntimeError as e:
    print("data fetching")
    GPIO.cleanup()

def get_rainfall():
    """Calculate and return the total rainfall in mm."""
    global rain_count
    rainfall= rain_count* RAIN_MM_PER_TIP
    rain_count = 0
    return rainfall

try:
    while True:
        time.sleep(60)
        rainfall= get_rainfall()
        print(f"Rainfall Detected: {rainfall:.2f}mm")
except KeyboardInterrupt:
    print("Stopping rainfall measurement...")
    GPIO.cleanup()