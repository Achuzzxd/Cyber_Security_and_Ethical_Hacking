import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from password_checker import analyze_password  
ACCENT_COLOR = "#00f7ff"

class CyberPasswordGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Password Strength Analyzer")
        self.root.geometry("900x700")
        self.root.configure(bg="#000000")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview",
                             background="#181c20",
                             foreground="#fff",
                             fieldbackground="#181c20",
                             font=('Consolas', 11))
        self.style.configure("Treeview.Heading",
                             background="#232946",
                             foreground=ACCENT_COLOR,
                             font=('Segoe UI', 12, 'bold'))
        self.style.map('Treeview', background=[('selected', ACCENT_COLOR)])

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="🔐 Cyber Password Strength Analyzer",
                         font=("Segoe UI", 22, "bold"), fg="#22c55e", bg="#000000")
        title.pack(pady=12)
        entry_frame = tk.Frame(self.root, bg="#000000")
        entry_frame.pack(pady=8)

        tk.Label(entry_frame, text="Enter Password:", font=("Segoe UI", 13, "bold"), fg=ACCENT_COLOR, bg="#000000").pack(side=tk.LEFT, padx=6)
        self.password_var = tk.StringVar()
        self.entry = tk.Entry(entry_frame, textvariable=self.password_var, font=("Consolas", 14, "bold"), width=30,
                              bg="#181c20", fg="#fff", insertbackground="#fff", relief="flat")
        self.entry.pack(side=tk.LEFT, padx=6)
        self.entry.bind("<Return>", lambda e: self.analyze())

        self.btn = tk.Button(entry_frame, text="Analyze", font=("Segoe UI", 12, "bold"),
                             bg=ACCENT_COLOR, fg="#000000", activebackground="#fbbf24", activeforeground="#000000", relief="flat",
                             command=self.analyze, padx=18, pady=2)
        self.btn.pack(side=tk.LEFT, padx=6)

        self.strength_label = tk.Label(self.root, text="", font=("Segoe UI", 20, "bold"), bg="#000000")
        self.strength_label.pack(pady=10)

        scores_frame = tk.Frame(self.root, bg="#000000")
        scores_frame.pack(pady=5, fill="x", padx=20)

        self.z_score_var = tk.StringVar()
        self.custom_score_var = tk.StringVar()
        self.transitions_score_var = tk.StringVar()

        tk.Label(scores_frame, text="zxcvbn score (out of 4):", font=("Segoe UI", 12, "bold"), fg=ACCENT_COLOR, bg="#000000").grid(row=0, column=0, sticky="w", padx=10)
        tk.Label(scores_frame, textvariable=self.z_score_var, font=("Consolas", 14, "bold"), fg="#df308d", bg="#000000").grid(row=1, column=0, sticky="w", padx=10)

        tk.Label(scores_frame, text="strength score (out of 4):", font=("Segoe UI", 12, "bold"), fg=ACCENT_COLOR, bg="#000000").grid(row=0, column=1, sticky="w", padx=10)
        tk.Label(scores_frame, textvariable=self.custom_score_var, font=("Consolas", 14, "bold"), fg="#df308d", bg="#000000").grid(row=1, column=1, sticky="w", padx=10)

        tk.Label(scores_frame, text="transitions score (out of 2):", font=("Segoe UI", 12, "bold"), fg=ACCENT_COLOR, bg="#000000").grid(row=0, column=2, sticky="w", padx=10)
        tk.Label(scores_frame, textvariable=self.transitions_score_var, font=("Consolas", 14, "bold"), fg="#df308d", bg="#000000").grid(row=1, column=2, sticky="w", padx=10)

        info_frame = tk.Frame(self.root, bg="#000000")
        info_frame.pack(pady=10, fill="both", expand=True, padx=20)

        left_col = tk.Frame(info_frame, bg="#000000")
        left_col.pack(side=tk.LEFT, fill="both", expand=True, padx=10)

        right_col = tk.Frame(info_frame, bg="#000000")
        right_col.pack(side=tk.LEFT, fill="both", expand=True, padx=10)

        self.z_sugg_tv = self.create_treeview(left_col, "zxcvbn Suggestions")
        self.custom_sugg_tv = self.create_treeview(left_col, "Custom Suggestions")
        self.trans_sugg_tv = self.create_treeview(left_col, "Transitions Suggestions")

        self.final_score_label = self.create_info_label(right_col, "Final Score (out of 100):")
        self.crack_time_label = self.create_info_label(right_col, "Crack Time (online throttling 100 per hour):")
        self.warning_label = self.create_info_label(right_col, "Warning:")
        self.guesses_label = self.create_info_label(right_col, "Guesses taken:")

        
        self.seq_details_text = self.create_text_box(right_col, "Sequence Details:", height=12)

    def create_treeview(self, parent, title):
        lbl = tk.Label(parent, text=title, font=("Segoe UI", 12, "bold"), fg=ACCENT_COLOR, bg="#000000")
        lbl.pack(anchor="w", pady=(10, 0))
        tv = ttk.Treeview(parent, columns=("Suggestion",), show="headings", height=6, style="Treeview")
        tv.heading("Suggestion", text="Suggestion")
        tv.column("Suggestion", anchor="w", width=280)
        tv.pack(fill="x", pady=4)
        return tv

    def create_info_label(self, parent, label_text):
        frame = tk.Frame(parent, bg="#000000")
        frame.pack(fill="x", pady=6)
        lbl = tk.Label(frame, text=label_text, font=("Segoe UI", 12, "bold"), fg=ACCENT_COLOR, bg="#000000")
        lbl.pack(side=tk.LEFT)
        val = tk.Label(frame, text="", font=("Consolas", 12, "bold"), fg="#fff", bg="#000000")
        val.pack(side=tk.LEFT, padx=6)
        return val

    def create_text_box(self, parent, label_text, height=6):
        lbl = tk.Label(parent, text=label_text, font=("Segoe UI", 12, "bold"), fg=ACCENT_COLOR, bg="#000000")
        lbl.pack(anchor="w", pady=(10, 0))
        txt = tk.Text(parent, height=height, wrap="word", font=("Consolas", 11), bg="#181c20", fg="#fff")
        txt.pack(fill="both", expand=True, pady=4)
        txt.config(state=tk.DISABLED)
        return txt

    def analyze(self):
        pwd = self.password_var.get()
        if not pwd:
            messagebox.showwarning("Input Error", "Please enter a password.")
            return

        res = analyze_password(pwd)

        
        color_map = {
            "Very Strong": "#22c55e",    
            "Strong": "#a3e635",         
            "Moderate": "#fbbf24",       
            "Weak": "#ef4444"            
        }
        self.strength_label.config(text=res['label'], fg=color_map.get(res['label'], "#22c55e"))

        self.z_score_var.set(f"{res['z_score']} / 4")
        self.custom_score_var.set(f"{res['custom_score']} / 4")
        self.transitions_score_var.set(f"{res['transitions score']} / 2")

        self.update_treeview(self.z_sugg_tv, res['z_suggestions'])
        self.update_treeview(self.custom_sugg_tv, res['custom_suggestions'])
        self.update_treeview(self.trans_sugg_tv, res['transitions_suggestions'])

        self.final_score_label.config(text=f"{res['final_score']:.1f}")
        self.crack_time_label.config(text=res['crack_time'])
        self.warning_label.config(text=res['warning'] or "None")
        self.guesses_label.config(text=f"{res['guesses']}")

        seqd_lines = []
        for idx, pattern in enumerate(res['sequence_details'], 1):
            seqd_lines.append(f"Pattern {idx}:")
            for k, v in pattern.items():
                seqd_lines.append(f"  {k}: {v}")
        self.set_text(self.seq_details_text, "\n".join(seqd_lines) if seqd_lines else "None")

    def update_treeview(self, tv, items):
        tv.delete(*tv.get_children())
        if not items:
            tv.insert("", "end", values=("None",))
        else:
            for item in items:
                tv.insert("", "end", values=(item,))

    def set_text(self, text_widget, content):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberPasswordGUI(root)
    root.mainloop()
