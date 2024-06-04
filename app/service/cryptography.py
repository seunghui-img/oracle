import base64
from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s : s + (BS - len(s.encode('utf-8')) % BS) * chr(BS - len(s.encode('utf-8')) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__(self, key):
        self.key = key
    
    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode('utf-8')))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))
    
key = [0x13, 0x11, 0xAA, 0x2B, 0xA5, 0x16, 0x5B, 0x33, 0xAA, 0xA3, 0x72, 0x45, 0x42, 0xEA, 0xBA, 0x13,
            0xA3, 0x43, 0xBA, 0xC1, 0xDE, 0xE3, 0x37, 0x4D, 0x3D, 0x18, 0x32, 0xB6, 0xA4, 0x3E, 0x12, 0xF3]

def Pay_MakeServiceValue(plain_data):
    encrypt_data = AESCipher(bytes(key)).encrypt(plain_data)
    return encrypt_data.decode('utf-8')

def Pay_GetServiceValue(encrypted_data):
    decrypted_data = AESCipher(bytes(key)).decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')
