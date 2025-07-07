import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import platform

from scanner import scan_windows, scan_linux
from gui.network_table import NetworkTable
from gui.signal_graph import SignalGraph
from gui.channel_graph import ChannelGraph
from gui.qr_popup import QRPopup
from utils.export import export_networks

class WifiScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wi-Fi Network Scanner")
        self.geometry("1080x720")
        self.configure(bg="#f5f6fa")
        self.networks = []
        self.auto_refresh_interval = 6000
        self.auto_refresh_enabled = False
        self.auto_refresh_job = None

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TLabel", font=("Segoe UI", 11), background="#f5f6fa")
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#273c75", background="#f5f6fa")
        style.configure("TFrame", background="#f5f6fa")

        header = ttk.Label(self, text="Wi-Fi Network Scanner", style="Header.TLabel")
        header.pack(pady=(18, 8))

        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=20, pady=(0, 12))

        self.scan_button = ttk.Button(top_frame, text="Scan Wi-Fi", command=self.scan_networks)
        self.scan_button.pack(side=tk.LEFT, padx=6)

        self.qr_button = ttk.Button(top_frame, text="Generate QR", command=self.generate_qr, state=tk.DISABLED)
        self.qr_button.pack(side=tk.LEFT, padx=6)

        self.export_button = ttk.Button(top_frame, text="Export", command=self.export_results)
        self.export_button.pack(side=tk.LEFT, padx=6)

        self.auto_refresh_button = ttk.Button(top_frame, text="Enable Auto-Refresh", command=self.toggle_auto_refresh)
        self.auto_refresh_button.pack(side=tk.LEFT, padx=6)

        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 12))

        self.network_table = NetworkTable(table_frame)
        self.network_table.pack(fill=tk.BOTH, expand=True)
        self.network_table.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        graphs_frame = ttk.LabelFrame(self, text="Network Visualization", padding=(12, 8))
        graphs_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 18))

        self.signal_graph = SignalGraph(graphs_frame)
        self.signal_graph.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8), pady=4)

        self.channel_graph = ChannelGraph(graphs_frame)
        self.channel_graph.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0), pady=4)

    def scan_networks(self):
        os_name = platform.system()
        if os_name == "Windows":
            networks = scan_windows.scan_windows_networks()
        elif os_name == "Linux":
            networks = scan_linux.scan_linux_networks()
        else:
            messagebox.showerror("Error", f"Unsupported OS: {os_name}")
            return

        self.networks = networks
        self.network_table.update_table(networks)
        self.signal_graph.plot(networks)
        self.channel_graph.plot(networks)
        self.qr_button.config(state=tk.DISABLED)

        if not networks:
            messagebox.showinfo("No Networks", "No Wi-Fi networks found.")

        if self.auto_refresh_enabled:
            self.auto_refresh_job = self.after(self.auto_refresh_interval, self.scan_networks)

    def toggle_auto_refresh(self):
        self.auto_refresh_enabled = not self.auto_refresh_enabled
        if self.auto_refresh_enabled:
            self.auto_refresh_button.config(text="Disable Auto-Refresh")
            if self.auto_refresh_job is None:
                self.auto_refresh_job = self.after(self.auto_refresh_interval, self.scan_networks)
        else:
            self.auto_refresh_button.config(text="Enable Auto-Refresh")
            if self.auto_refresh_job is not None:
                self.after_cancel(self.auto_refresh_job)
                self.auto_refresh_job = None

    def on_row_select(self, event):
        selected = self.network_table.get_selected_network()
        if selected:
            self.qr_button.config(state=tk.NORMAL)
        else:
            self.qr_button.config(state=tk.DISABLED)

    def generate_qr(self):
        selected = self.network_table.get_selected_network()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a network first.")
            return
        ssid = selected.get("ssid")
        security = selected.get("security")
        password = ""
        if security.lower() not in ("open", "nopass", "unknown"):
            password = simpledialog.askstring("Wi-Fi Password", f"Enter password for {ssid}:", show="*")
        QRPopup.show(self, ssid, security, password)

    def export_results(self):
        if not self.networks:
            messagebox.showinfo("No Data", "No scan results to export.")
            return
        filetypes = [("CSV files", "*.csv"), ("PDF files", "*.pdf")]
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=filetypes)
        if not filepath:
            return
        if filepath.endswith(".csv"):
            export_networks(self.networks, filepath, "csv")
        elif filepath.endswith(".pdf"):
            export_networks(self.networks, filepath, "pdf")
        else:
            messagebox.showerror("Error", "Unsupported file type.")

if __name__ == "__main__":
    app = WifiScannerApp()
    app.mainloop()
