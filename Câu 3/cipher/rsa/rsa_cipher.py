
import os
import rsa

class RSACipher:
    def __init__(self):
        self.key_dir = os.path.join(os.path.dirname(__file__), "keys")
        if not os.path.exists(self.key_dir):
            os.makedirs(self.key_dir)
            
        self.private_key_path = os.path.join(self.key_dir, "private_key.pem")
        self.public_key_path = os.path.join(self.key_dir, "public_key.pem")

    def generate_keys(self):
        public_key, private_key = rsa.newkeys(1024)

        with open(self.public_key_path, "wb") as f:
            f.write(public_key.save_pkcs1())

        with open(self.private_key_path, "wb") as f:
            f.write(private_key.save_pkcs1())

    def load_keys(self):
        with open(self.private_key_path, "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
            
        with open(self.public_key_path, "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
            
        return private_key, public_key

    def encrypt(self, message, key):
        return rsa.encrypt(message.encode('ascii'), key) # public_key

    def decrypt(self, ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode('ascii') # private_key
        except:
            return False

    def sign(self, message, key):
        # Ký số thông điệp sử dụng hàm hash 'SHA-256'
        return rsa.sign(message.encode('ascii'), key, 'SHA-256') # private_key

    def verify(self, message, signature, key):
        # Xác minh chữ ký số
        try:
            # Hàm rsa.verify thành công sẽ trả về chuỗi tên thuật toán hash (VD: 'SHA-256')
            return rsa.verify(message.encode('ascii'), signature, key) == 'SHA-256' # public_key
        except:
            return False