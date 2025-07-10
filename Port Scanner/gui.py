import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading

from port_scanner import scan_ports

# --- Callback for colored output ---
def gui_callback_factory(output_area):
    def gui_callback(msg, color):
        output_area.config(state='normal')
        output_area.insert(tk.END, msg, color)
        output_area.see(tk.END)
        output_area.config(state='disabled')
    return gui_callback

# --- Scan logic ---
def start_scan():
    target = entry_target.get().strip()
    start_port = entry_start.get().strip()
    end_port = entry_end.get().strip()

    output_area.config(state='normal')
    output_area.delete('1.0', tk.END)
    output_area.config(state='disabled')

    # Input validation
    if not target or not start_port or not end_port:
        messagebox.showwarning("Missing Fields", "Please fill in all fields.")
        return

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        messagebox.showerror("Invalid Host", "Could not resolve hostname.")
        return

    try:
        start_port_int = int(start_port)
        end_port_int = int(end_port)
        if not (0 <= start_port_int <= 65535 and 0 <= end_port_int <= 65535):
            raise ValueError
        if start_port_int > end_port_int:
            messagebox.showerror("Port Error", "Start port must be less than or equal to end port.")
            return
    except ValueError:
        messagebox.showerror("Port Error", "Ports must be valid numbers between 0 and 65535.")
        return

    output_area.config(state='normal')
    output_area.insert(tk.END, f"Scanning {target} ({ip}) from port {start_port_int} to {end_port_int}...\n\n", "info")
    output_area.config(state='disabled')

    def threaded_scan():
        # Custom callback for colored output
        def colored_callback(msg):
            if "[OPEN]" in msg:
                color = "open"
            elif "[CLOSED]" in msg:
                color = "closed"
            else:
                color = "info"
            gui_callback(msg, color)
        scan_ports(
            ip,
            start_port_int,
            end_port_int,
            callback=colored_callback
        )
        output_area.config(state='normal')
        output_area.insert(tk.END, "\nScanning completed.\n", "info")
        output_area.config(state='disabled')

    gui_callback = gui_callback_factory(output_area)
    threading.Thread(target=threaded_scan, daemon=True).start()

# --- UI Setup ---
root = tk.Tk()
root.title("Port Scanner")
root.geometry("560x560")
root.configure(bg="#181818")
root.resizable(True, True)

font_label = ("Segoe UI", 12)
font_entry = ("Consolas", 13)
font_result = ("Consolas", 12)

# --- Entry fields with Enter navigation ---
def on_entry_enter(event, next_widget=None):
    if next_widget:
        next_widget.focus_set()
    else:
        start_scan()

label_fg = "#cccccc"
entry_bg = "#222222"
entry_fg = "#00ffcc"
entry_bd = 2

tk.Label(root, text="Target IP / Domain:", bg="#181818", fg=label_fg, font=font_label).pack(pady=(20, 4))
entry_target = tk.Entry(root, width=38, font=font_entry, bg=entry_bg, fg=entry_fg, bd=entry_bd, insertbackground=entry_fg)
entry_target.pack(pady=4)
entry_target.focus_set()

tk.Label(root, text="Start Port:", bg="#181818", fg=label_fg, font=font_label).pack(pady=(16, 4))
entry_start = tk.Entry(root, width=15, font=font_entry, bg=entry_bg, fg=entry_fg, bd=entry_bd, insertbackground=entry_fg)
entry_start.pack(pady=4)

tk.Label(root, text="End Port:", bg="#181818", fg=label_fg, font=font_label).pack(pady=(16, 4))
entry_end = tk.Entry(root, width=15, font=font_entry, bg=entry_bg, fg=entry_fg, bd=entry_bd, insertbackground=entry_fg)
entry_end.pack(pady=4)

# Bind Enter keys for field navigation and scan
entry_target.bind("<Return>", lambda e: on_entry_enter(e, entry_start))
entry_start.bind("<Return>", lambda e: on_entry_enter(e, entry_end))
entry_end.bind("<Return>", lambda e: on_entry_enter(e, None))

tk.Button(root, text="Start Scan", bg="#00aaff", fg="white", font=("Segoe UI", 12, "bold"),
          activebackground="#007799", activeforeground="#ffffff", command=start_scan, bd=0, padx=12, pady=6).pack(pady=18)

output_area = scrolledtext.ScrolledText(root, width=66, height=18, font=font_result, bg="#111111", fg="#ffffff", bd=2, relief="flat", state='disabled')
output_area.pack(pady=10)

# Tag configuration for colored output
output_area.tag_config("open", foreground="#00ff00")
output_area.tag_config("closed", foreground="#ffffff")
output_area.tag_config("info", foreground="#00aaff")

root.mainloop()
