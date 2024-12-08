import serial
import time

# Cấu hình cổng serial (thay /dev/ttyUSB0 bằng COMx nếu trên Windows)
arduino_port = "COM3"  # Ví dụ: COM3 hoặc /dev/ttyUSB0
baud_rate = 9600       # Tốc độ baud phải khớp với Arduino
timeout = 1            # Thời gian chờ khi không nhận dữ liệu

# Kết nối với Arduino
ser = serial.Serial(arduino_port, baud_rate, timeout=timeout)
print("Connected to Arduino:", arduino_port)

time.sleep(2)  # Đợi Arduino khởi động

# Gửi dữ liệu đến Arduino
data_to_send = "Hello Arduino\n"
ser.write(data_to_send.encode())
print(f"Sent: {data_to_send.strip()}")

# Nhận dữ liệu từ Arduino
while True:
    data_received = ser.readline().decode().strip()  # Đọc một dòng dữ liệu
    if data_received:
        print(f"Received: {data_received}")
        break

# Đóng cổng serial khi xong
ser.close()
print("Serial connection closed.")
