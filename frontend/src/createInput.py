import tkinter as tk

def Input(root,
          textColor:str,
          bgColor:str,
          width:int):
    entry = tk.Entry(root, font=('Helvetica', 25),fg=textColor,background=bgColor,width=width,)
    return entry


