import tkinter as tk
from tkinter import ttk
from utils.security_icons import get_security_color, get_security_label

class NetworkTable(ttk.Frame):
    def __init__(self, parent, columns=None):
        super().__init__(parent)
        if columns is None:
            columns = ("SSID", "BSSID", "Signal", "Channel", "Security")
        self.columns = columns

        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._init_security_tags()

    def _init_security_tags(self):
        for color in ["darkgreen", "green", "limegreen", "orange", "red", "gray"]:
            self.tree.tag_configure(color, foreground=color)

    def update_table(self, networks):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for net in networks:
            sec_type = net.get("security", "")
            sec_label = get_security_label(sec_type)
            color = get_security_color(sec_type)
            row_values = (
                net.get("ssid", ""),
                net.get("bssid", ""),
                net.get("signal", ""),
                net.get("channel", ""),
                sec_label
            )
            self.tree.insert("", tk.END, values=row_values, tags=(color,))

    def get_selected_network(self):
        selected = self.tree.selection()
        if not selected:
            return None
        values = self.tree.item(selected[0])["values"]
        return dict(zip([col.lower() for col in self.columns], values))
