import tkinter as tk

def codeArea(root):
    codeText = tk.Text(root, wrap=tk.WORD, font=("Courier", 15,"bold"), bg="black", fg="white",padx=20, pady=13)
    codeText.config(state=tk.DISABLED)

    # codeText.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    return codeText