import tkinter as tk
from tkinter import messagebox
from predict import predict_urls

def on_predict(event=None):
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("🚫 Input Error", "Please enter a URL.")
        return

    try:
        result = predict_urls([url])
        _, prediction = result[0]

        result_label.config(
            text=f"🔍 Result: {prediction}",
            fg="green" if prediction == "Legitimate" else "red"
        )
    except Exception as e:
        messagebox.showerror("❗ Prediction Error", str(e))

root = tk.Tk()
root.title("🔐 Phishing URL Detector")
root.geometry("500x250")
root.config(bg="#000000")  

title_label = tk.Label(
    root, 
    text="🔐 Phishing URL Checker", 
    font=("Helvetica", 18, "bold"), 
    fg="#FFFFFF",
    bg="#000000"
)
title_label.pack(pady=15)

url_entry = tk.Entry(root, font=("Helvetica", 14), width=40)
url_entry.pack(pady=10)
url_entry.focus()

url_entry.bind('<Return>', on_predict)

predict_button = tk.Button(
    root, 
    text="Analyze URL", 
    font=("Helvetica", 12), 
    bg="#0B0E8C", 
    fg="#FFFFFF", 
    command=on_predict
)
predict_button.pack(pady=10)

result_label = tk.Label(
    root, 
    text="", 
    font=("Helvetica", 14), 
    bg="#000000"
)
result_label.pack(pady=10)

root.mainloop()
