from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

def update_table(self):
    """Thêm dữ liệu vào table_result và căn giữa các giá trị."""
    # Cập nhật bảng với tiêu đề cột
    self.mainHandle.table_result.setItem(0, 0, QtWidgets.QTableWidgetItem("STT"))
    self.mainHandle.table_result.setItem(0, 1, QtWidgets.QTableWidgetItem("Name"))
    self.mainHandle.table_result.setItem(0, 2, QtWidgets.QTableWidgetItem("Age"))
    
    # Căn giữa tiêu đề cột
    self.mainHandle.table_result.item(0, 0).setTextAlignment(Qt.AlignCenter)
    self.mainHandle.table_result.item(0, 1).setTextAlignment(Qt.AlignCenter)
    self.mainHandle.table_result.item(0, 2).setTextAlignment(Qt.AlignCenter)
    
    # Thêm các dòng dữ liệu
    data = [
        ["1", "John", "25"],
        ["2", "Jane", "30"],
        ["3", "Sam", "22"]
    ]
    
    for row, row_data in enumerate(data, start=1):  # Bắt đầu từ dòng 1 vì dòng 0 đã dùng cho tiêu đề
        for col, value in enumerate(row_data):
            item = QtWidgets.QTableWidgetItem(value)
            self.mainHandle.table_result.setItem(row, col, item)
            # Căn giữa các giá trị trong các dòng dữ liệu
            self.mainHandle.table_result.item(row, col).setTextAlignment(Qt.AlignCenter)
