import tkinter as tk
from createButton import Button
from createInput import Input
from codeArea import codeArea
from textArea import textArea
import requests
from tkinter import messagebox

def handleButton():
    text.config(state=tk.NORMAL)
    code.config(state=tk.NORMAL)
    # text.insert(tk.END,"Generating...")
    question = entryField.get()
    url = "http://localhost:3000/chatbot"
    data = {"question":question}
    if (question ==""):
        messagebox.showwarning("Input error","please enter a valid input")
        # text.pack_forget()
        # code.pack_forget()
        return
    try:
        res = requests.post(url=url, json=data)
        genText = res.json()
        diff = genText[:3]
        if diff == "```":
            text.pack_forget()
            code.pack(anchor="center", expand=True, fill=tk.BOTH, padx=10, pady=10)
            copyButton.pack(pady=2)
            code.delete(1.0, tk.END)  
            code.insert(tk.END,genText)
            code.config(state=tk.DISABLED)
        else:
            code.pack_forget()
            text.pack(anchor="center", expand=True, fill=tk.BOTH, padx=10, pady=10)
            text.delete(1.0, tk.END)  
            text.insert(tk.END,genText)
            text.config(state=tk.DISABLED)

    except requests.exceptions.RequestException as e:
        print(e)
        text.pack_forget()
        code.pack_forget()
        # text.delete(1.0,tk.END)
        # text.config(state=tk.DISABLED)
        messagebox.showerror("Error","something went wrong")
def copyHandler():
    root.clipboard_clear()
    text = code.get("1.0", tk.END)
    goodText = text.split("```")
    print(goodText)
    root.clipboard_append(goodText[1])
root = tk.Tk()
root.title("Electron")
root.geometry("3000x500")
root.configure(bg="gray11")


entryField = Input(root,textColor="white",bgColor="gray13", width=70)

entryField.pack(pady=20,padx=10,)


genButton = Button(root, height=1,text="GO", width=5,bgColor="red2", textColor="white",bold=20, 
handleButton=handleButton )

genButton.pack(pady=10)


copyButton = Button(root, height=1, width=4, bgColor="gray78", textColor="black",bold=15, handleButton=copyHandler,text="copy")


code = codeArea(root)


text = textArea(root)



root.mainloop()