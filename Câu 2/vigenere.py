import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic

# =====================================================================
# 1. CLASS THUẬT TOÁN VIGENERE (CỦA BẠN)
# =====================================================================
class VigenereCipher:
    def vigenere_encrypt(self, plain_text, key):
        if not key:
            return ""
        encrypted_text = ""
        key_index = 0
        for char in plain_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)].upper()) - ord('A')
                if char.isupper():
                    encrypted_text += chr((ord(char) - ord('A') + key_shift) % 26 + ord('A'))
                else:
                    encrypted_text += chr((ord(char) - ord('a') + key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def vigenere_decrypt(self, encrypted_text, key):
        if not key:
            return ""
        decrypted_text = ""
        key_index = 0
        for char in encrypted_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)].upper()) - ord('A')
                if char.isupper():
                    decrypted_text += chr((ord(char) - ord('A') - key_shift) % 26 + ord('A'))
                else:
                    decrypted_text += chr((ord(char) - ord('a') - key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text


# =====================================================================
# 2. CLASS QUẢN LÝ GIAO DIỆN UI
# =====================================================================
class VigenereApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Tự động tìm đường dẫn chính xác vào thư mục ui/vigenere_ui.ui
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, 'ui', 'vigenere_ui.ui')
        
        # Tải file giao diện đồ họa trực tiếp
        uic.loadUi(ui_path, self)
        self.setWindowTitle("VIGENERE CIPHER TOOL")
        
        # Khởi tạo đối tượng xử lý thuật toán mã hóa
        self.cipher = VigenereCipher()
        
        # Kết nối sự kiện Click của nút bấm trên Qt Designer với hàm xử lý
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_decrypt.clicked.connect(self.handle_decrypt)

    def get_widget_text(self, widget):
        """Hàm bổ trợ tự động nhận diện kiểu dữ liệu của ô nhập (LineEdit hoặc TextEdit) 
        để tránh lỗi không gõ được chữ hoặc đơ form"""
        if hasattr(widget, 'toPlainText'):
            return widget.toPlainText().strip()
        elif hasattr(widget, 'text'):
            return widget.text().strip()
        return ""

    def set_widget_text(self, widget, text):
        """Hàm bổ trợ tự động ghi dữ liệu ra màn hình tương thích với mọi loại ô hiển thị"""
        if hasattr(widget, 'setPlainText'):
            widget.setPlainText(text)
        elif hasattr(widget, 'setText'):
            widget.setText(text)

    def handle_encrypt(self):
        # Đọc dữ liệu đầu vào linh hoạt từ UI
        plain_text = self.get_widget_text(self.txt_plain_encrypt)
        key = self.get_widget_text(self.txt_key_encrypt)
        
        if not plain_text or not key:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ văn bản và Key mã hóa!")
            return
            
        # Thực hiện xử lý thuật toán offline trực tiếp
        cipher_text = self.cipher.vigenere_encrypt(plain_text, key)
        
        # Xuất kết quả ra giao diện
        self.set_widget_text(self.txt_result_cipher, cipher_text)

    def handle_decrypt(self):
        # Đọc dữ liệu đầu vào linh hoạt từ UI
        cipher_text = self.get_widget_text(self.txt_cipher_decrypt)
        key = self.get_widget_text(self.txt_key_decrypt)
        
        if not cipher_text or not key:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ văn bản mã hóa và Key!")
            return
            
        # Thực hiện xử lý thuật toán giải mã offline trực tiếp
        plain_text = self.cipher.vigenere_decrypt(cipher_text, key)
        
        # Xuất kết quả ra giao diện
        self.set_widget_text(self.txt_result_plain, plain_text)


# =====================================================================
# 3. KÍCH HOẠT ỨNG DỤNG
# =====================================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec_())