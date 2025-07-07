import os
import base64
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def run_decryption():
    
        password = "Achyutha"
    
        with open("key_salt.bin","rb") as f:
            salt = f.read()

        kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length=32, salt = salt, iterations = 50000, backend = default_backend)

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        fernet = Fernet(key)

        original_folder = "view_files"
        hidden_folder = "dest_files"    

        for filename in os.listdir(hidden_folder):
            filepath = os.path.join(hidden_folder, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, "rb") as file:
                        encrypted_data = file.read()
                    decrypted_data = fernet.decrypt(encrypted_data)
            
                    destpath = os.path.join(original_folder, filename)
                    with open(destpath, "wb") as file:
                        file.write(decrypted_data)

                    os.remove(filepath)
                except:
                    print("Failure")
        return "Success"

def decrypt_files():
    password = "Achyutha"
    
    with open("key_salt.bin","rb") as f:
        salt = f.read()

    kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length=32, salt = salt, iterations = 50000, backend = default_backend)

    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    fernet = Fernet(key)

    original_folder = "view_files"   

    for filename in os.listdir(original_folder):
        filepath = os.path.join(original_folder, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, "rb") as file:
                    encrypted_data = file.read()
                decrypted_data = fernet.decrypt(encrypted_data)
            
                destpath = os.path.join(original_folder, filename)
                with open(destpath, "wb") as file:
                    file.write(decrypted_data)
            except:
                print("Failure")
    return "Success"
             
def decrypt_folder(pwd):
    
    if pwd=="Decryptyourfolder":
        original_folder = "view_files"
        hidden_folder = "dest_files"
        for filename in os.listdir(hidden_folder):
                filepath = os.path.join(hidden_folder, filename)
                if os.path.isfile(filepath):
                    try:
                        with open(filepath, "rb") as file:
                            encrypted_data = file.read()
                        destpath = os.path.join(original_folder, filename)
                        with open(destpath, "wb") as file:
                            file.write(encrypted_data)
                        os.remove(filepath)
                    except:
                        print("Failure")
        return "Success"