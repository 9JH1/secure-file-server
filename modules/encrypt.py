import hashlib
from os import walk
from os.path import join
from cryptography.fernet import Fernet
import base64
fernet = ""

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def set_key(a):
    global fernet
    fernet = Fernet(a)

def list_directory(path):
    result = []
    for root, dirs, files in walk(path):
        for file in files:
            result.append(join(root, file).replace(path,""))
    return result

def encrypt_file(path):
    global fernet
    with open(path,'rb') as file:
        first = file.read()
    second = fernet.encrypt(first)
    with open(path, 'wb') as file:
        file.write(second)
    print("encrypted: " + path)

def decrypt_file(path):
    global fernet
    with open(path,'rb') as file:
        first = file.read()
    second = fernet.decrypt(first)
    with open(path, 'wb') as file:
        file.write(second)
    print("decrypted: "+path)

def encrypt_directory(path):
    for root, dirs, files in walk(path):
        for file in files:
            full_path = join(root, file)
            encrypt_file(full_path)

def decrypt_directory(path):
    for root, dirs, files in walk(path):
        for file in files:
            full_path = join(root, file)
            decrypt_file(full_path)

def decrypt_file_return_string(path):
    global fernet
    with open(path,'rb') as file:
        first = file.read()
    second = fernet.decrypt(first)
    print("decrypted: " + path)
    return second

def decrypt_file_return_string_base64(path):
    global fernet
    with open(path,'rb') as file:
        first = file.read()
    second = fernet.decrypt(first)
    print("decrypted: " + path)
    base64_data = base64.b64encode(second)
    base64_string = base64_data.decode("utf-8")
    return base64_string

def decrypt_directory_return_string(path):
    # dict where key is file extension :D
    result = {}
    for root, dirs, files in walk(path):
        for file in files:
            ext = file.split('.')
            ext = ext[len(ext)-1]
            result[ext] = decrypt_file_return_string(join(root, file))
    return result

def decrypt_directory_return_string_base64(path):
    # dict where key is file extension :D
    result = {}
    for root, dirs, files in walk(path):
        for file in files:
            ext = file.split('.')
            ext = ext[len(ext)-1]
            
            second = decrypt_file_return_string(join(root, file))
            base64_data = base64.b64encode(second)
            base64_string = base64_data.decode("utf-8")
            result[ext] = base64_string
    return result