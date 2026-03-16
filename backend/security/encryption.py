from Crypto.Cipher import AES
import base64, os

KEY = os.urandom(32)

def pad(s): return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
def unpad(s): return s[:-ord(s[-1])]

def encrypt(text: str):
    cipher = AES.new(KEY, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad(text).encode())).decode()

def decrypt(enc: str):
    cipher = AES.new(KEY, AES.MODE_ECB)
    return unpad(cipher.decrypt(base64.b64decode(enc)).decode())
