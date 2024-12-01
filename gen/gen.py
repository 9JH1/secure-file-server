from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode

password = b"your_password_here"  # Your password as bytes
salt = b"your_salt_here"     # Use a unique, random salt (16 bytes recommended)
iterations = 100_000         # Number of iterations (100,000+ is standard)

# Derive the key 
kdf = PBKDF2HMAC(
    algorithm=SHA256(),
    length=32,
    salt=salt,
    iterations=iterations,
    backend=default_backend()
)
key = urlsafe_b64encode(kdf.derive(password))  # Fernet key must be URL-safe and base64-encoded

print(key)
