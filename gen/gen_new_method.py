from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
from hashlib import sha256
from sys import argv
from time import sleep
password = ""
if(len(argv)>3):
    exit(1)
for argument in range(len(argv)):
    if argv[argument] == "--password":
        password = argv[argument + 1]
def encrypt_string(hash_string):
    sha_signature = sha256(str(hash_string).encode()).hexdigest()
    return sha_signature
salt = ''.join(reversed(encrypt_string(password))).encode()
iterations = 100_000
kdf = PBKDF2HMAC(
    algorithm=SHA256(),
    length=32,
    salt=salt,
    iterations=iterations,
    backend=default_backend()
)
key = urlsafe_b64encode(kdf.derive(password.encode()))
sleep(5)
print(str(key)[2:-1])