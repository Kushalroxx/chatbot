import tkinter as tk

def codeArea(root):
    codeText = tk.Text(root, wrap=tk.NONE, font=("Courier", 12), bg="black", fg="white")
    codeText.config(state=tk.DISABLED)

    # codeText.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    return codeText