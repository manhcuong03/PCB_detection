import serial
import time

class ArduinoSerial:
    def __init__(self, port="COM5", baudrate=9600, timeout=1):
        """
        Khởi tạo đối tượng Serial kết nối với Arduino.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        """
        Mở kết nối Serial.
        """
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Đã kết nối tới {self.port} với tốc độ {self.baudrate}")
            time.sleep(1)  # Chờ Arduino khởi động
        except Exception as e:
            print(f"Lỗi khi kết nối: {e}")

    def send_command(self, command):
        """
        Gửi lệnh tới Arduino.
        """
        if self.connection and self.connection.is_open:
            try:
                self.connection.write((command + '\n').encode('utf-8'))  # Thêm ký tự xuống dòng
                print(f"Đã gửi lệnh: {command}")
            except Exception as e:
                print(f"Lỗi khi gửi lệnh: {e}")
        else:
            print("Kết nối Serial chưa được mở.")

    def read_response(self):
        """
        Đọc phản hồi từ Arduino.
        """
        if self.connection and self.connection.is_open:
            try:
                if self.connection.in_waiting > 0:
                    response = self.connection.readline().decode('utf-8').strip()
                    return response
            except Exception as e:
                print(f"Lỗi khi đọc phản hồi: {e}")
        else:
            print("Kết nối Serial chưa được mở.")
        return None

    def close(self):
        """
        Đóng kết nối Serial.
        """
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Đã đóng kết nối Serial.")
        else:
            print("Kết nối Serial đã đóng hoặc chưa được mở.")

# Sử dụng lớp ArduinoSerial
if __name__ == "__main__":
    arduino = ArduinoSerial(port="COM5", baudrate=9600)
    arduino.connect()

    # Gửi lệnh và đọc phản hồi
    arduino.send_command("01")  # Gửi lệnh "00" đến Arduino
    response = arduino.read_response()
    if response:
        print(f"Phản hồi từ Arduino: {response}")

    # Đóng kết nối
    arduino.close()
