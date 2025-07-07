import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import Counter

class ChannelGraph(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax.set_title("Wi-Fi Channel Usage", pad=15)
        self.ax.set_xlabel("Channel")
        self.ax.set_ylabel("Number of Networks")
        self.figure.tight_layout()

    def plot(self, networks):
        self.ax.clear()
        channels = [net.get("channel") for net in networks if net.get("channel") is not None]
        if not channels:
            self.ax.set_title("Wi-Fi Channel Usage", pad=15)
            self.ax.set_xlabel("Channel")
            self.ax.set_ylabel("Number of Networks")
            self.ax.text(0.5, 0.5, "No Data", ha='center', va='center', fontsize=14, transform=self.ax.transAxes)
            self.figure.tight_layout()
            self.canvas.draw()
            return
        channel_counts = Counter(channels)
        sorted_channels = sorted(channel_counts.keys())
        counts = [channel_counts[ch] for ch in sorted_channels]
        bars = self.ax.bar([str(ch) for ch in sorted_channels], counts, color='orange')
        self.ax.set_title("Wi-Fi Channel Usage", pad=15)
        self.ax.set_xlabel("Channel")
        self.ax.set_ylabel("Number of Networks")
        self.ax.set_ylim(0, max(counts + [1]))
        self.ax.set_xticks(range(len(sorted_channels)))
        self.ax.set_xticklabels([str(ch) for ch in sorted_channels], fontsize=9)
        for bar, count in zip(bars, counts):
            self.ax.annotate(f"{count}", xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                             xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)
        self.figure.tight_layout()
        self.canvas.draw()
