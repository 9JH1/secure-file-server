from cryptography.fernet import Fernet
key = b'G8fOBhGTmZ7UHTO28UZGn4lAEvQz473Ct8rPKqJDlA4='

try:
    f = Fernet(key)  # Try to initialize a Fernet object
    print("Valid Fernet key!")
except ValueError as e:
    print(f"Invalid Fernet key: {e}")
 