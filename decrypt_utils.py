# decrypt_utils.py

from Crypto.Cipher import AES
import base64

def pad_key(key: str) -> bytes:
    return key.ljust(32)[:32].encode("utf-8")

def decrypt_question(encrypted_data: str, key: str) -> str:
    try:
        key_bytes = pad_key(key)
        encrypted_data_bytes = base64.b64decode(encrypted_data)

        iv = encrypted_data_bytes[:16]
        ciphertext = encrypted_data_bytes[16:]

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        decrypted_bytes = cipher.decrypt(ciphertext)

        # Remove null padding manually
        decrypted_text = decrypted_bytes.rstrip(b"\0").decode("utf-8", errors="replace")
        return decrypted_text

    except Exception as e:
        return f"Decryption failed: {str(e)}"
