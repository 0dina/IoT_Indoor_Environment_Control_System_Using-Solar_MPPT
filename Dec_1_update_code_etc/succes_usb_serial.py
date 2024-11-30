import serial
import time

try:
    # CDC-ACM 포트 설정
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
    print("Serial port opened successfully.")

    # 데이터 송신
    send_data = "Hello ACM UART!"
    ser.write(send_data.encode())
    print(f"Sent: {send_data}")

    # 데이터 수신 대기
    time.sleep(2)
    print("Waiting for data...")

    while True:
        if ser.in_waiting > 0:
            received_data = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Received: {received_data}")
        
        time.sleep(1)

except serial.SerialException as e:
    print(f"Serial error: {e}")

except Exception as e:
    print(f"Error: {e}")

finally:
    if ser and ser.is_open:
        ser.close()
        print("Serial port closed.")