import os
from base64 import urlsafe_b64encode

# Password (your secret input)
password = b"test"

# Generate a random, unique salt
salt = os.urandom(16)  # 16 bytes is standard
print("Password:", password)
print("Salt:", urlsafe_b64encode(salt))  # Optional: encode for easier storage
