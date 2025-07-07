import tkinter as tk
from tkinter import Toplevel, Label, Button, messagebox
import qrcode
from PIL import Image, ImageTk

def generate_wifi_qr_string(ssid, security, password=None):
    if security.lower().startswith("wpa"):
        security_type = "WPA"
    elif security.lower().startswith("wep"):
        security_type = "WEP"
    else:
        security_type = "nopass"
    password = password or ""

    return f"WIFI:T:{security_type};S:{ssid};P:{password};;"

class QRPopup(Toplevel):
    def __init__(self, parent, ssid, security, password=None):
        super().__init__(parent)
        self.title(f"QR Code for {ssid}")
        self.geometry("320x400")
        self.resizable(False, False)
        self.ssid = ssid
        self.security = security
        self.password = password

        
        qr_data = generate_wifi_qr_string(ssid, security, password)
        qr_img = qrcode.make(qr_data)
        qr_img = qr_img.resize((300, 300), Image.LANCZOS)
        self.qr_photo = ImageTk.PhotoImage(qr_img)

        
        self.label = Label(self, text=f"Scan to join:\n{ssid}", font=("Arial", 12))
        self.label.pack(pady=10)
        self.qr_label = Label(self, image=self.qr_photo)
        self.qr_label.pack(pady=10)

        
        self.close_button = Button(self, text="Close", command=self.destroy)
        self.close_button.pack(pady=10)

    @staticmethod
    def show(parent, ssid, security, password=None):
        if not ssid:
            messagebox.showerror("Error", "No SSID provided for QR code.")
            return
        popup = QRPopup(parent, ssid, security, password)
        popup.grab_set()

