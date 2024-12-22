import snap7
from snap7.util import get_int, set_int

class SiemensPLC:
    def __init__(self, ip, rack=0, slot=1):
        
        # Khởi tạo đối tượng SiemensPLC.
        # :param ip: Địa chỉ IP của PLC.
        # :param rack: Rack của PLC (mặc định là 0).
        # :param slot: Slot của PLC (mặc định là 1).
        
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.client = snap7.client.Client()

    def connect(self):
        
        # Kết nối tới PLC.
        
        try:
            self.client.connect(self.ip, self.rack, self.slot)
            if self.client.get_connected():
                print(f"Kết nối thành công tới PLC tại {self.ip}!")
            else:
                print("Không thể kết nối tới PLC.")
        except Exception as e:
            print(f"Lỗi khi kết nối: {e}")

    def disconnect(self):
        
        # Ngắt kết nối khỏi PLC.
        
        try:
            self.client.disconnect()
            print("Đã ngắt kết nối khỏi PLC.")
        except Exception as e:
            print(f"Lỗi khi ngắt kết nối: {e}")

    def read_data(self, db_number, start, size):
        
        # Đọc dữ liệu từ Data Block (DB) của PLC.
        # :param db_number: Số DB (Data Block).
        # :param start: Offset bắt đầu.
        # :param size: Kích thước dữ liệu cần đọc (byte).
        # :return: Dữ liệu đã đọc (bytearray).
        
        try:
            data = self.client.db_read(db_number, start, size)
            value = get_int(data, 0)  # Giả sử đọc INT tại offset 0
            print(f"Dữ liệu đọc được từ DB{db_number}, offset {start}: {value}")
            print("type", type(value))
            return value
        except Exception as e:
            print(f"Lỗi khi đọc dữ liệu: {e}")
            return None

    def write_data(self, db_number, start, value):
    
        # Ghi dữ liệu vào Data Block (DB) của PLC.
        # :param db_number: Số DB (Data Block).
        # :param start: Offset bắt đầu.
        # :param value: Giá trị cần ghi (INT).

        try:
            data = bytearray(2)  # INT chiếm 2 byte
            set_int(data, 0, value)
            self.client.db_write(db_number, start, data)
            print(f"Đã ghi giá trị {value} vào DB{db_number}, offset {start}.")
        except Exception as e:
            print(f"Lỗi khi ghi dữ liệu: {e}")

# Sử dụng class
if __name__ == "__main__":
    # Thông tin kết nối
    plc_ip = "192.168.0.1"  # Địa chỉ IP của PLC
    rack = 0
    slot = 1
    db_number = 1  # Số DB (Data Block)
    start = 0      # Offset bắt đầu
    size = 2      # Kích thước dữ liệu (INT = 2 byte)

    # Tạo đối tượng PLC
    plc = SiemensPLC(plc_ip, rack, slot)

    # Kết nối tới PLC
    plc.connect()
    data = "01"
    plc.write_data(db_number, start, data)
    plc.read_data(3, 0, 2)

    # Ngắt kết nối
    plc.disconnect()
