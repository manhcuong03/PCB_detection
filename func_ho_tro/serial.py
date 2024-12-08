import serial
import time

class UI:
    def __init__(self, arduino_port="COM3", baud_rate=9600, timeout=1):
        # Khởi tạo cổng serial và các tham số
        self.arduino_port = arduino_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        # Kết nối với Arduino
        self.ser = serial.Serial(self.arduino_port, self.baud_rate, timeout=self.timeout)
        print("Connected to Arduino:", self.arduino_port)
        time.sleep(2)  # Đợi Arduino khởi động

    def send_data(self, data_to_send):
        # Gửi dữ liệu đến Arduino
        if self.ser and self.ser.is_open:
            self.ser.write(data_to_send.encode())
            print(f"Sent: {data_to_send.strip()}")
        else:
            print("No connection to Arduino.")

    def receive_data(self):
        # Nhận dữ liệu từ Arduino
        if self.ser and self.ser.is_open:
            while True:
                data_received = self.ser.readline().decode().strip()  # Đọc một dòng dữ liệu
                if data_received:
                    print(f"Received: {data_received}")
                    return data_received
        else:
            print("No connection to Arduino.")
            return None

    def close_connection(self):
        # Đóng cổng serial khi xong
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed.")
        else:
            print("No connection to close.")

# Sử dụng UI class
ui = UI()  # Khởi tạo đối tượng UI với tham số mặc định
ui.connect()  # Kết nối với Arduino

# Gửi và nhận dữ liệu
ui.send_data("00")  # Ví dụ gửi dữ liệu "00"
received_data = ui.receive_data()  # Nhận dữ liệu từ Arduino

ui.close_connection()  # Đóng kết nối
