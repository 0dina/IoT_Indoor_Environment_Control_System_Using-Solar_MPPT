from gpiozero import Button
import time
import math

# Global variables
wind_count = 0  # Counts how many half-rotations
radius_cm = 9.0  # Radius of your anemometer
wind_interval = 5  # How often (secs) to report speed
CM_IN_A_KM = 100000.0  # Centimeters in a kilometer
SECS_IN_AN_HOUR = 3600  # Seconds in an hour
ADJUSTMENT = 1.18  # Adjustment factor for anemometer accuracy

# Every half-rotation, add 1 to count
def spin():
    global wind_count
    wind_count += 1
    # print("spin" + str(wind_count))

# Calculate the wind speed
def calculate_speed(time_sec):
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0  # Convert half-rotations to full rotations
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR
    return km_per_hour * ADJUSTMENT

# Reset the wind count
def reset_wind():
    global wind_count
    wind_count = 0

# Setup wind speed sensor
wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = spin

# Loop to measure wind speed and report at intervals
while True:
    reset_wind()  # Reset the count
    time.sleep(wind_interval)  # Wait for the interval
    speed = calculate_speed(wind_interval)  # Calculate wind speed
    print(f"Wind Speed: {speed:.2f} km/h")
