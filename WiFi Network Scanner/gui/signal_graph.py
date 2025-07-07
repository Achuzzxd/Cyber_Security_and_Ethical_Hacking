import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SignalGraph(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax.set_title("Wi-Fi Signal Strengths", pad=15)
        self.ax.set_xlabel("SSID")
        self.ax.set_ylabel("Signal (%)")
        self.figure.tight_layout()

    def plot(self, networks):
        self.ax.clear()
        ssids = [net.get("ssid", "") for net in networks]
        signals = [net.get("signal", 0) for net in networks]
        bars = self.ax.bar(ssids, signals, color='skyblue')
        self.ax.set_title("Wi-Fi Signal Strengths", pad=15)
        self.ax.set_xlabel("SSID")
        self.ax.set_ylabel("Signal (%)")
        self.ax.set_ylim(0, 100)
        self.ax.set_xticks(range(len(ssids)))
        self.ax.set_xticklabels(ssids, rotation=30, ha='right', fontsize=9)
        for bar, signal in zip(bars, signals):
            y = bar.get_height()
            if y > 90:
                self.ax.annotate(f"{signal}", xy=(bar.get_x() + bar.get_width() / 2, y - 5),
                                 xytext=(0, 0), textcoords="offset points",
                                 ha='center', va='top', fontsize=8, color="black")
            else:
                self.ax.annotate(f"{signal}", xy=(bar.get_x() + bar.get_width() / 2, y),
                                 xytext=(0, 3), textcoords="offset points",
                                 ha='center', va='bottom', fontsize=8, color="black")
        self.figure.tight_layout()
        self.canvas.draw()
