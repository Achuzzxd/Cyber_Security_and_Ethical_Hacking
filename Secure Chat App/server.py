import socket
import threading

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 65432

clients = []

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def forward_message(sender_sock):
    while True:
        try:
            length_bytes = recvall(sender_sock, 4)
            if not length_bytes:
                print(f"[-] Client disconnected")
                break
            msg_len = int.from_bytes(length_bytes, byteorder='big')

            message = recvall(sender_sock, msg_len)
            if not message:
                print(f"[-] Client disconnected")
                break

            for client in clients:
                if client != sender_sock:
                    client.sendall(length_bytes + message)
        except Exception as e:
            print(f"[!] Error: {e}")
            break

    if sender_sock in clients:
        clients.remove(sender_sock)
    sender_sock.close()
    print("[-] Connection closed")

def start_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((SERVER_HOST, SERVER_PORT))
    server_sock.listen(2)
    print(f"[*] Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while len(clients) < 2:
        client_sock, addr = server_sock.accept()
        print(f"[+] Client connected from {addr}")
        clients.append(client_sock)

    for client_sock in clients:
        threading.Thread(target=forward_message, args=(client_sock,), daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[!] Server shutting down.")
    finally:
        for c in clients:
            c.close()
        server_sock.close()

if __name__ == "__main__":
    start_server()
