import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import subprocess
import sys
import socket
import time

from crypto_utils import generate_rsa_keys, encrypt_message, decrypt_message
from Crypto.PublicKey import RSA

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

BG_COLOR = "#121212"
SYS_MSG_COLOR = "#FFA500"
USER1_YOU_COLOR = "#1E90FF"
USER1_PEER_COLOR = "#32CD32"
USER2_YOU_COLOR = "#32CD32"
USER2_PEER_COLOR = "#1E90FF"
INPUT_FG_COLOR = "#FFFFFF"
BUTTON_BG = "#1F1F1F"
BUTTON_ACTIVE_BG = "#333333"
BUTTON_FG = "#FFFFFF"
FONT_TITLE = ("Segoe UI", 28, "bold")
FONT_NOTE = ("Segoe UI", 12, "italic")
FONT_LABEL = ("Segoe UI", 16, "bold")
FONT_STATUS = ("Segoe UI", 10, "italic")
FONT_CHAT = ("Consolas", 11)
FONT_INPUT = ("Consolas", 11)

class ServerManager:
    def __init__(self):
        self.process = None

    def start(self):
        try:
            self.process = subprocess.Popen([sys.executable, "server.py"],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            text=True,
                                            bufsize=1)
            threading.Thread(target=self._read_server_output, daemon=True).start()
            return True
        except Exception as e:
            print(f"[!] Failed to start server: {e}")
            return False

    def _read_server_output(self):
        if self.process and self.process.stdout:
            for line in iter(self.process.stdout.readline, ''):
                print(f"[SERVER_LOG] {line.strip()}")
            self.process.stdout.close()

    def stop(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print("[SERVER] Server process terminated.")

class ChatClientGUI:
    def __init__(self, master, name, you_color, peer_color, system_color):
        self.master = master
        self.name = name
        self.you_color = you_color
        self.peer_color = peer_color
        self.system_color = system_color

        self.frame = tk.Frame(master, bd=2, relief=tk.RIDGE, bg=BG_COLOR, highlightbackground="#444", highlightthickness=1)

        self.sock = None
        self.private_key = None
        self.public_key = None
        self.peer_public_key = None

        self.connected = False
        self.keys_exchanged = False

        self.build_ui()

    def build_ui(self):
        top_bar = tk.Frame(self.frame, bg=BG_COLOR)
        top_bar.pack(fill=tk.X, padx=15, pady=(10, 5))

        user_label = tk.Label(top_bar, text=self.name, font=FONT_LABEL, fg=self.you_color, bg=BG_COLOR)
        user_label.pack(side=tk.LEFT)

        self.connect_button = tk.Button(
            top_bar, text="Connect to Server", command=self.start_connection_thread,
            bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_FG,
            relief=tk.FLAT, padx=10, pady=5
        )
        self.connect_button.pack(side=tk.LEFT, padx=15)

        self.status_label = tk.Label(
            top_bar, text="Disconnected", fg="red", bg=BG_COLOR, font=FONT_STATUS
        )
        self.status_label.pack(side=tk.LEFT, padx=15)

        self.chat_area = scrolledtext.ScrolledText(
            self.frame, state='disabled', wrap='word', height=20, width=50,
            bg="#181818", fg="white", font=FONT_CHAT, borderwidth=0, highlightthickness=0
        )
        self.chat_area.pack(padx=15, pady=(0, 5), fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(self.frame, bg=BG_COLOR)
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.msg_entry = tk.Entry(
            input_frame, width=40, state='disabled', fg=INPUT_FG_COLOR, bg="#222222",
            insertbackground=INPUT_FG_COLOR, font=FONT_INPUT, relief=tk.FLAT, highlightthickness=1, highlightbackground="#444"
        )
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.msg_entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = tk.Button(
            input_frame, text="Send", command=self.send_message, state='disabled',
            bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_FG,
            relief=tk.FLAT, padx=15, pady=6
        )
        self.send_button.pack(side=tk.LEFT)

    def display_message(self, msg, msg_type="system"):
        if msg_type == "system":
            color = self.system_color
        elif msg_type == "you":
            color = self.you_color
        else:
            color = self.peer_color
        self.master.after(0, lambda: self._append_message_to_chat(msg, color))

    def _append_message_to_chat(self, msg, color):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + "\n", (color,))
        self.chat_area.tag_config(color, foreground=color)
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def update_status(self, text, color):
        self.master.after(0, lambda: self.status_label.config(text=text, fg=color))

    def enable_input(self):
        self.master.after(0, lambda: self.msg_entry.config(state='normal'))
        self.master.after(0, lambda: self.send_button.config(state='normal'))

    def disable_input(self):
        self.master.after(0, lambda: self.msg_entry.config(state='disabled'))
        self.master.after(0, lambda: self.send_button.config(state='disabled'))

    def start_connection_thread(self):
        self.connect_button.config(state='disabled')
        self.update_status("Connecting...", SYS_MSG_COLOR)
        self.display_message("[+] Connecting to server...", "system")
        threading.Thread(target=self._connect_and_exchange_keys, daemon=True).start()

    def _connect_and_exchange_keys(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((SERVER_HOST, SERVER_PORT))
            self.connected = True
            self.display_message("[+] Connected to server.", "system")
            self.update_status("Connected", "#4CAF50")

            self.private_key, self.public_key = generate_rsa_keys()

            self.display_message("[*] Sending public key to peer...", "system")
            pub_key_bytes = self.public_key.export_key(format='PEM')
            self.sock.sendall(len(pub_key_bytes).to_bytes(4, byteorder='big'))
            self.sock.sendall(pub_key_bytes)
            self.display_message("[*] Sent public key to peer.", "system")

            self.display_message("[*] Waiting for peer's public key...", "system")
            peer_len_bytes = self.recvall(4)
            peer_len = int.from_bytes(peer_len_bytes, byteorder='big')
            peer_pub_key_bytes = self.recvall(peer_len)

            self.peer_public_key = RSA.import_key(peer_pub_key_bytes)
            self.keys_exchanged = True
            self.display_message("[*] Successfully imported peer's public key.", "system")
            self.display_message("You can start typing messages.", "system")

            self.enable_input()

            threading.Thread(target=self.receive_messages, daemon=True).start()

        except Exception as e:
            self.display_message(f"[!] Connection or Key Exchange Error: {e}", "system")
            self.update_status("Disconnected", "#F44336")
            self.connected = False
            self.keys_exchanged = False
            self.master.after(0, lambda: self.connect_button.config(state='normal'))
            self.close_socket()
            self.disable_input()

    def recvall(self, n):
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                raise ConnectionError("Connection closed unexpectedly by remote host.")
            data += packet
        return data

    def receive_messages(self):
        while True:
            try:
                length_bytes = self.recvall(4)
                if not length_bytes:
                    raise ConnectionError("Peer closed connection.")

                msg_len = int.from_bytes(length_bytes, byteorder='big')
                encrypted_msg = self.recvall(msg_len)
                decrypted_msg = decrypt_message(encrypted_msg, self.private_key)
                self.display_message(f"Peer: {decrypted_msg}", "peer")
            except Exception as e:
                self.display_message(f"[!] Chat session ended: {e}", "system")
                self.update_status("Disconnected", "#F44336")
                self.connected = False
                self.keys_exchanged = False
                self.disable_input()
                self.close_socket()
                self.master.after(0, lambda: self.connect_button.config(state='normal'))
                break

    def send_message(self):
        if not self.connected or not self.keys_exchanged:
            messagebox.showwarning(self.name, "Not connected or keys not exchanged yet.")
            return

        msg = self.msg_entry.get().strip()
        if not msg:
            return
        try:
            encrypted_msg = encrypt_message(msg, self.peer_public_key)
            self.sock.sendall(len(encrypted_msg).to_bytes(4, byteorder='big'))
            self.sock.sendall(encrypted_msg)
            self.display_message(f"You: {msg}", "you")
            self.msg_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror(self.name, f"Failed to send message: {e}")
            self.display_message(f"[!] Send error: {e}", "system")
            self.update_status("Error Sending", "#F44336")
            self.disable_input()
            self.close_socket()

    def close_socket(self):
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            except OSError:
                pass
            finally:
                self.sock = None

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Chat Demo App")
        self.root.configure(bg=BG_COLOR)

        self.server_manager = ServerManager()

        tk.Label(root, text="Secure Chat Demo App", font=FONT_TITLE,
                 fg="white", bg=BG_COLOR).pack(pady=(15,5))

        note_text = ("Note: In this demo, both users are shown in the same application window for demonstration purposes.\n"
                     "In a real-world scenario, these users would be on separate devices and locations.")
        tk.Label(root, text=note_text, font=FONT_NOTE,
                 fg=SYS_MSG_COLOR, bg=BG_COLOR, justify=tk.CENTER).pack(pady=(0,15))

        self.activate_server_button = tk.Button(root, text="Activate Server", command=self.activate_server,
                                                width=20, height=2,
                                                bg=BUTTON_BG, fg=BUTTON_FG,
                                                activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_FG)
        self.activate_server_button.pack(pady=10)

        self.clients_container = tk.Frame(root, bg=BG_COLOR)

        self.user1 = ChatClientGUI(self.clients_container, "User 1", USER1_YOU_COLOR, USER1_PEER_COLOR, SYS_MSG_COLOR)
        self.user2 = ChatClientGUI(self.clients_container, "User 2", USER2_YOU_COLOR, USER2_PEER_COLOR, SYS_MSG_COLOR)

        self.user1.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.user2.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def activate_server(self):
        self.activate_server_button.config(state='disabled', text="Server Active")
        self.root.update_idletasks()

        if self.server_manager.start():
            time.sleep(0.5)
            self.clients_container.pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showerror("Server Error", "Failed to activate server.")
            self.activate_server_button.config(state='normal', text="Activate Server")

    def on_closing(self):
        self.user1.close_socket()
        self.user2.close_socket()
        self.server_manager.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
