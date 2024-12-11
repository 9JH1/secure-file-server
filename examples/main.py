from cryptography.fernet import Fernet
from time import sleep
try:
    # Key for encryption/decryption
    key = b'kvcUlT96rO3bKwU0O6TcEDUSbqHuKSam98P8uuTdN_4='
    fernet = Fernet(key)

    # Encrypt and decrypt helper functions
    def decrypt_file(path):
        with open(path, 'rb') as f: return fernet.decrypt(f.read()).decode()

    def encrypt_string(text): return fernet.encrypt(text.encode())

    # Main logic
    with open('./lock', 'r+b') as f:
        content = f.read() or f.write(encrypt_string("1000"))
        f.seek(0)

    e = int(decrypt_file('./lock'))
    for a in range(e):
        print(e - a)
        sleep(1)
        with open('./lock', 'wb') as f:
            f.write(encrypt_string(str(e - a)))
    if(decrypt_file('./lock')=="1"):
        print(key)
except Exception as e:
    print("error occured, Delete lock and try again ;)")