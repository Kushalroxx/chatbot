import tkinter as tk

def textArea(root):
    text = tk.Text(root, wrap=tk.NONE, font=("Courier", 12),background="gray78", fg="black")
    text.config(state=tk.DISABLED)

    # text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    return text