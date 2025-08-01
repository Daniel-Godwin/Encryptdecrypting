# crypto_utils.py

from Crypto.Cipher import AES
import base64
import os

def pad_key(key: str) -> bytes:
    return key.ljust(32)[:32].encode("utf-8")

def encrypt_question(question_text: str, key: str) -> str:
    key_bytes = pad_key(key)
    iv = os.urandom(16)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)

    # Pad to multiple of 16 using null bytes
    padded = question_text.encode("utf-8")
    while len(padded) % 16 != 0:
        padded += b"\0"

    encrypted = cipher.encrypt(padded)
    return base64.b64encode(iv + encrypted).decode("utf-8")
