import hashlib
from os import walk
from os.path import join
from cryptography.fernet import Fernet
import base64

fernet = None

def encrypt_string(hash_string):
    try:
        return hashlib.sha256(hash_string.encode()).hexdigest()
    except Exception as e:
        print(f"Error in encrypt_string: {e}")
        return None

def set_key(a):
    global fernet
    try:
        fernet = Fernet(a)
    except Exception as e:
        print(f"Error setting key: {e}")

def list_directory(path):
    try:
        return [join(root, file).replace(path, "") for root, _, files in walk(path) for file in files]
    except Exception as e:
        print(f"Error listing directory: {e}")
        return []

def encrypt_file(path):
    try:
        with open(path, 'rb') as file:
            first = file.read()
        encrypted = fernet.encrypt(first)
        with open(path, 'wb') as file:
            file.write(encrypted)
        print(f"encrypted: {path}")
    except Exception as e:
        print(f"Error encrypting file {path}: {e}")

def decrypt_file(path):
    try:
        with open(path, 'rb') as file:
            first = file.read()
        decrypted = fernet.decrypt(first)
        with open(path, 'wb') as file:
            file.write(decrypted)
        print(f"decrypted: {path}")
    except Exception as e:
        print(f"Error decrypting file {path}: {e}")

def encrypt_directory(path):
    for root, _, files in walk(path):
        for file in files:
            encrypt_file(join(root, file))

def decrypt_directory(path):
    for root, _, files in walk(path):
        for file in files:
            decrypt_file(join(root, file))

def decrypt_file_return_string(path):
    try:
        with open(path, 'rb') as file:
            first = file.read()
        decrypted = fernet.decrypt(first)
        print(f"decrypted: {path}")
        return decrypted
    except Exception as e:
        print(f"Error decrypting file {path}: {e}")
        return None

def encrypt_string_return_string(string):
    try:
        return fernet.encrypt(string.encode())
    except Exception as e:
        print(f"Error encrypting string: {e}")
        return None

def decrypt_string_return_string(string):
    try:
        return fernet.decrypt(string.decrypt())
    except Exception as e:
        print(f"Error decrypting string: {e}")
        return None

def decrypt_file_return_string_base64(path):
    try:
        with open(path, 'rb') as file:
            first = file.read()
        decrypted = fernet.decrypt(first)
        base64_string = base64.b64encode(decrypted).decode("utf-8")
        print(f"decrypted: {path}")
        return base64_string
    except Exception as e:
        print(f"Error in decrypt_file_return_string_base64: {e}")
        return None

def decrypt_directory_return_string(path):
    result = {}
    try:
        for root, _, files in walk(path):
            for file in files:
                ext = file.split('.')[-1]
                result[ext] = decrypt_file_return_string(join(root, file))
    except Exception as e:
        print(f"Error in decrypt_directory_return_string: {e}")
    return result

def decrypt_directory_return_string_base64(path):
    result = {}
    try:
        for root, _, files in walk(path):
            for file in files:
                ext = file.split('.')[-1]
                decrypted = decrypt_file_return_string(join(root, file))
                if decrypted:
                    base64_string = base64.b64encode(decrypted).decode("utf-8")
                    result[ext] = base64_string
    except Exception as e:
        print(f"Error in decrypt_directory_return_string_base64: {e}")
    return result
