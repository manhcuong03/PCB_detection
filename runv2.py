from PyQt5.QtWidgets import QApplication, QMainWindow
from loginHandle import LOGIN_HANDLE
from mainHandle import MAIN_HANDLE
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from ultralytics import YOLO
import cv2
import time
import os
from serial_communication import ArduinoSerial
from plc import SiemensPLC
class UI(): 
    def __init__(self):
        self.mainUI = QMainWindow()
        self.mainHandle = MAIN_HANDLE(self.mainUI)
        self.mainHandle.btnLogout.clicked.connect(lambda: self.loadLoginForm())
        self.loginUI = QMainWindow()
        self.loginHandle = LOGIN_HANDLE(self.loginUI)
        self.loginHandle.btnLogin.clicked.connect(lambda: self.loadMainForm(0))
        self.loginUI.show()
        # arduino ------------------------------------------------
        self.control = ArduinoSerial()
        self.control.connect()
        # self.control.send_command("00")
        #arduino -------------------------------------------------
        self.mainHandle.btn00.clicked.connect(self.send00)
        self.mainHandle.btn01.clicked.connect(self.send01)
        # PLC --------------------------------------------------
        plc_ip = "192.168.0.1"  # Địa chỉ IP của PLC
        rack = 0
        slot = 1
        db_number = 1  # Số DB (Data Block)
        start = 0      # Offset bắt đầu
        size = 2       # Kích thước dữ liệu (INT = 2 byte)
        self.controlPLC = SiemensPLC(plc_ip, rack, slot)
        self.controlPLC.connect()
        # self.startXla()
        # PLC --------------------------------------------------
        # Date and time -----------------------------------------
        self.mainHandle.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.timer = QTimer(self.mainUI)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # Cập nhật mỗi giây
        # Date and time -----------------------------------------
        
        # Biến camera và timer-----------------------------------
        self.cap = None
        self.timer = QTimer()
        self.mainHandle.btnCapture.clicked.connect(lambda: self.capture_image())
        
        # # Bảng giá trị -------------------------------------------
        # self.mainHandle.table_result.setItem(0, 0, QtWidgets.QTableWidgetItem("STT"))
        # self.mainHandle.table_result.setItem(0, 1, QtWidgets.QTableWidgetItem("Capacitor"))
        # self.mainHandle.table_result.setItem(0, 2, QtWidgets.QTableWidgetItem("IC"))

        # Load YOLO model
        weight = 'best_mo.pt'
        self.model = YOLO(weight)
        #     # Căn giữa tiêu đề cột
        # self.mainHandle.table_result.item(0, 0).setTextAlignment(Qt.AlignCenter)
        # self.mainHandle.table_result.item(0, 1).setTextAlignment(Qt.AlignCenter)
        # self.mainHandle.table_result.item(0, 2).setTextAlignment(Qt.AlignCenter)
        # Đảm bảo bảng có đúng số cột và tiêu đề
        self.mainHandle.table_result.setColumnCount(4)
        self.mainHandle.table_result.setHorizontalHeaderLabels(["Số thứ tự", "IC", "Capacitor", "Connector"])
        self.mainHandle.table_result.setRowCount(0)  # Xóa tất cả các dòng ban đầu
        self.mainHandle.table_result.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # # Bảng giá trị -------------------------------------------
        self.controlPLC.write_data(3,0,0)
    # hàm xử lý ảnh được thực hiện khi có giá trị data db3 0 2 từ 0 lên 1
    def startXla(self):
        if self.controlPLC.read_data(3, 0, 2) == 1:
            # Thực hiện các lệnh khi có sự thay đổi
            self.controlPLC.write_data(3, 0, 0)
            self.capture_image()

    # các giao diện chính       
    def loadMainForm(self, data):
        self.loginUI.hide()
        self.mainUI.show()
        self.start_camera()
    def loadLoginForm(self):
        self.mainUI.hide()
        self.loginUI.show()
        self.stop_camera()
    def update_datetime(self):
        """Cập nhật ngày giờ trên QDateTimeEdit."""
        current_datetime = QDateTime.currentDateTime()
        self.mainHandle.dateTimeEdit.setDateTime(current_datetime)
    # arduino -------------------------------------------------
    def send00(self):
        self.control.send_command("00")
    def send01(self):
        self.control.send_command("01")  
    # arduino -------------------------------------------------

    # camera ---------------------------------------------------
    def start_camera(self):
        """Khởi động camera và bắt đầu hiển thị hình ảnh."""
        if not self.cap:
            self.cap = cv2.VideoCapture(1)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Cập nhật mỗi 30ms
    def update_frame(self):
        """Cập nhật hình ảnh từ camera lên QLabel."""
        ret, frame = self.cap.read()
        if ret:
            # self.startXla()
            if self.controlPLC.read_data(3,0,2) == 1:
                self.controlPLC.write_data(3,0,00)
                self.capture_image()
            # Chuyển đổi hình ảnh từ BGR (OpenCV) sang RGB (Qt)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.mainHandle.lbl_img.setPixmap(pixmap)  # Hiển thị trên QLabel
            self.mainHandle.lbl_img.setScaledContents(True)  # Đảm bảo ảnh vừa khung
    def stop_camera(self):
        """Dừng camera khi không cần nữa."""
        if self.cap:
            self.timer.stop()
            self.cap.release()
            self.cap = None
    def __del__(self):
        """Hủy tài nguyên khi thoát chương trình."""
        self.stop_camera()

    # camera --------------------------------------------------------------------------------------

    def capture_image(self):
    # ""Chụp ảnh từ camera và lưu vào biến.""
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                # Lưu hình ảnh đã chụp
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                capture_path = os.path.join(r'D:\code\Final_xla\UI\img_capture', f'captured_image_{timestamp}.jpg')
                cv2.imwrite(capture_path, frame)
                print(f"Ảnh đã được lưu tại: {capture_path}")

                # Gọi hàm dự đoán và cập nhật bảng
                self.predict_and_update_table(capture_path)

    def predict_and_update_table(self, image_path):
        """Dự đoán ảnh, lưu kết quả và cập nhật bảng dữ liệu."""

        # Predict on the image
        results = self.model.predict(image_path, show=False)

        # Initialize counters
        ic_count, capacitor_count, connector_count = 0, 0, 0

        # Extract predictions
        for result in results:
            predictions = result.boxes
            labels = predictions.cls.cpu().numpy()  # Labels
            for label in labels:
                if label == 0:  # capacitor
                    capacitor_count += 1
                elif label == 1:  # connector
                    connector_count += 1
                elif label == 2:  # ic
                    ic_count += 1

            # Lưu ảnh sau khi dự đoán
            processed_image = result.plot()  # Vẽ kết quả dự đoán
            timestamp = time.strftime("%Y%m%d_%H%M%S")  # Tạo timestamp
            output_dir = r'D:\code\Final_xla\UI\output'  # Thư mục lưu kết quả
            os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
            output_image_path = os.path.join(output_dir, f'output_image_{timestamp}.jpg')
            cv2.imwrite(output_image_path, processed_image)  # Lưu ảnh
            print(f"Ảnh dự đoán được lưu tại: {output_image_path}")

        # Cập nhật bảng `table_result`
        self.update_table_data(ic_count, capacitor_count, connector_count)



    def update_table_data(self, ic_count, capacitor_count, connector_count):
        """Cập nhật dữ liệu vào bảng."""
        row_position = self.mainHandle.table_result.rowCount()
        self.mainHandle.table_result.insertRow(row_position)  # Thêm một dòng mới

        # Dữ liệu để thêm vào bảng
        data = [row_position, ic_count, capacitor_count, connector_count]  # Cột đầu là Số thứ tự (STT)
        if(ic_count > 4): 
            self.send00()
        else:
            self.send01()
        # Duyệt qua từng cột và thêm giá trị
        for column, value in enumerate(data):
            item = QtWidgets.QTableWidgetItem(str(value))  # Chuyển thành chuỗi
            item.setTextAlignment(Qt.AlignCenter)  # Căn giữa nội dung
            self.mainHandle.table_result.setItem(row_position, column, item)
        self.writePLC()
    def writePLC(self):
        data = "01"
        self.controlPLC.write_data(1,0,data)



if __name__ == "__main__":
    app = QApplication([])
    
    ui = UI()
    
    app.exec_()
