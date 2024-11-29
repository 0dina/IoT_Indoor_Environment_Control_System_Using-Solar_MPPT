import RPi.GPIO as GPIO
import time

class RainSensor:
    RAIN_MM_PER_TIP = 0.2794  # Millimeters of rain per tip of the rain gauge

    def __init__(self, pin):
        self.rain_pin = pin
        self.rain_count = 0

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setup(self.rain_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Event detection for rain gauge tipping bucket
        try:
            GPIO.add_event_detect(self.rain_pin, GPIO.FALLING, callback=self.rain_callback)
        except RuntimeError as e:
            print("Error setting up rain gauge event detection:", e)
            GPIO.cleanup()

    def rain_callback(self, channel):
        """Callback function to increment rain count."""
        self.rain_count += 1

    def get_rainfall(self):
        """Calculate and return the total rainfall in mm."""
        rainfall = self.rain_count * self.RAIN_MM_PER_TIP
        self.rain_count = 0  # Reset rain count after reading
        return rainfall

    def cleanup(self):
        """Clean up GPIO resources."""
        GPIO.cleanup()
