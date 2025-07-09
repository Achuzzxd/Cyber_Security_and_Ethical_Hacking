import socket
import threading
import sys
from crypto_utils import generate_rsa_keys, encrypt_message, decrypt_message
from Crypto.PublicKey import RSA

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

class SecureChatClient:
    def __init__(self, host, port):
        self.server_host = host
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key, self.public_key = generate_rsa_keys()
        self.peer_public_key = None

    def connect(self):
        print(f"[+] Connecting to server {self.server_host}:{self.server_port}...")
        self.sock.connect((self.server_host, self.server_port))
        print("[+] Connected to server.")

        self.exchange_keys()

        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.send_messages()

    def exchange_keys(self):
        pub_key_bytes = self.public_key.export_key(format='PEM')
        pub_key_len = len(pub_key_bytes)

        self.sock.send(pub_key_len.to_bytes(4, byteorder='big'))
        self.sock.send(pub_key_bytes)
        print("[*] Sent public key to peer.")

        peer_len_bytes = self.recvall(4)
        if not peer_len_bytes:
            raise ConnectionError("Failed to receive peer public key length")
        peer_len = int.from_bytes(peer_len_bytes, byteorder='big')

        peer_pub_key_bytes = self.recvall(peer_len)
        if not peer_pub_key_bytes:
            raise ConnectionError("Failed to receive peer public key bytes")

        print(f"[*] Received peer public key ({len(peer_pub_key_bytes)} bytes):")
        print(peer_pub_key_bytes.decode(errors='ignore'))

        self.peer_public_key = RSA.import_key(peer_pub_key_bytes)
        print("[*] Successfully imported peer's public key.")

    def recvall(self, n):
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                raise ConnectionError("Connection closed unexpectedly")
            data += packet
        return data

    def receive_messages(self):
        while True:
            try:
                length_bytes = self.recvall(4)
                msg_len = int.from_bytes(length_bytes, byteorder='big')
                encrypted_msg = self.recvall(msg_len)

                decrypted_msg = decrypt_message(encrypted_msg, self.private_key)
                print(f"\n[Peer]: {decrypted_msg}\n> ", end='', flush=True)
            except Exception as e:
                print(f"\n[!] Error receiving message: {e}")
                print("[*] Closing connection.")
                self.sock.close()
                break

    def send_messages(self):
        print("You can start typing messages. Press Ctrl+C to exit.")
        try:
            while True:
                msg = input("> ")
                if not msg.strip():
                    continue

                encrypted_msg = encrypt_message(msg, self.peer_public_key)
                msg_len = len(encrypted_msg)

                self.sock.send(msg_len.to_bytes(4, byteorder='big'))
                self.sock.send(encrypted_msg)
        except KeyboardInterrupt:
            print("\n[!] Exiting chat.")
            self.sock.close()
            sys.exit(0)

if __name__ == "__main__":
    client = SecureChatClient(SERVER_HOST, SERVER_PORT)
    client.connect()
