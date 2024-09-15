import tkinter as tk

def Input(root,
          textColor:str,
          bgColor:str,
          width:int):
    entry = tk.Text(root,height = 2, font=('Helvetica', 25),fg=textColor,background=bgColor,width=width,padx = 0)
    return entry


