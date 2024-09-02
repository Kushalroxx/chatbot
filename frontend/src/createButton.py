import tkinter as tk

def Button(
        root,
        height,
        width: int, 
        text: str,
        bgColor:str, 
        textColor:str,
        bold:int,handleButton
        ): 
    button = tk.Button(
        root,               
        text=text,
        height=height,
        width=width,
        background=bgColor,
        fg=textColor,
        font=('Helvetica',bold,"bold"),
        activebackground=bgColor,
        activeforeground=textColor,
        border=1,
        command=handleButton
    )
    
    return button
