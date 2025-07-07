import os
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def run_encryption():
    password = "Achyutha"

    salt = os.urandom(16)
    with open("key_salt.bin","wb") as f:
        f.write(salt)

    kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length=32, salt = salt, iterations = 50000, backend = default_backend)

    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    fernet = Fernet(key)

    original_folder = "target_files"
    hidden_folder = "dest_files"

    for filename in os.listdir(original_folder):
        filepath = os.path.join(original_folder, filename)
        if os.path.isfile(filepath):
            with open(filepath, "rb") as file:
                data = file.read()
            encrypted_data = fernet.encrypt(data)
        
            destpath = os.path.join(hidden_folder, filename)
            with open(destpath, "wb") as file:
                file.write(encrypted_data)

            os.remove(filepath)


