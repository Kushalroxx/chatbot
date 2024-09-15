import tkinter as tk
from createButton import Button
from createInput import Input
from codeArea import codeArea
from textArea import textArea
import requests
from tkinter import messagebox
from label import createLabel
import os
import threading
import sys

url = "http://localhost:3000/chatbot"

def historyCall():
    historyUrl = "http://localhost:3000/history"
    token = ""
    with open("token.txt", "r") as file:
        token = file.read()
    history = ""
    try:
        history = requests.post(historyUrl, json = {"token":token})
    except Exception as e:
        return messagebox.showerror("Error", e)
    if history.status_code == 200:
        if "data" in history.json():
            newHistory = history.json()["data"]
            newHistory.reverse()
            historyText.config(state=tk.NORMAL)
            historyText.delete("1.0", "end")
            for i in range(len(history.json()["data"])):
                historyText.insert(tk.END, f"{i+1}) {newHistory[i]}\n")
            historyText.config(state=tk.DISABLED)
        else:
            historyText.config(state=tk.NORMAL)
            historyText.delete("1.0", "end")
            historyText.insert(tk.END, "No history found")
            historyText.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", history.json()["message"])

def chatbotHandler(genInput,genButton,headingText,logoutButton,code,text,historyText,loading):
    headingText.grid(row=1, column=1, pady=0, padx=0)
    logoutButton.grid(row=0, column=1, pady=0, padx=10)
    genInput.grid(row=0, column=0, pady=0, padx=0)
    genButton.grid(row=1, column=0, pady=0, padx=0)
    historyText.grid(row=2, column=1, pady=0, padx=0)
    
    historyCall()
def handleSignin():
    url = "http://localhost:3000/login"
    verifyUrl = "http://localhost:3000/login/verify"
    email=""
    # function to Reset
    def handleReset():
        python = sys.executable  
        os.execv(python, [python] + sys.argv)
    # function to handle otp submit
    def handleOtpSubmit():
       otp = otpField.get()
       loading.grid(row=3, column=1, pady=0)
       root.update_idletasks()  
       if not otp:
          return messagebox.showerror("Error", "Please enter your otp") 
       data = {"email":email,"otp":otp}
       def verifyOtp():
        try:
            response = requests.post(verifyUrl, json=data)
            if response.status_code == 200:
                with open("token.txt", "w") as file:
                    file.write(response.json()["token"])
                otpHeading.grid_remove()
                otpField.grid_remove()
                otpSubmitButton.grid_remove()
                resetButton.grid_remove()
                chatbotHandler(genInput,genButton,headingText,logoutButton,code,text,historyText,loading)
                
            else:
                messagebox.showerror("Error", response.json()["message"])
        except Exception as e:
            messagebox.showerror("Error", e)
        finally:
            loading.grid_remove()    
       threading.Thread(target=verifyOtp).start()
#  handle email and send otp
    email = emailField.get()
    if not email:
        messagebox.showerror("Error", "Please enter your email")
    data = {"email":email}
    loading.grid(row=3, column=0, pady=0)
    root.update_idletasks()  
    response = ""
    try:
        response = requests.post(url, json = data)
    except Exception as e:
        loading.grid_remove()
        return messagebox.showerror("Error", e)
    loading.grid_remove()
    if response.status_code == 200:
        # hiding the login widgets
        heading.grid_remove()
        emailField.grid_remove()
        submitButton.grid_remove()
        # showing the otp widgets
        otpHeading = tk.Label(root, bg="gray87", text="Enter OTP", font=("Arial", 34, "bold"))
        otpField = tk.Entry(root, width=20, font=("Helvetica", 25, "bold"), bg="gray80", fg="black")
        resetButton = tk.Button( root,
        text="Reset",
        font=("Arial", 17, "bold"),
        bg="red3",            
        fg="white",
        command=handleReset,              
        activebackground="red1",   
        activeforeground="white")
        otpSubmitButton = tk.Button( root,
        text="Submit",
        font=("Arial", 17, "bold"),
        bg="red3",            
        fg="white",
        command=handleOtpSubmit,              
        activebackground="red1",   
        activeforeground="white")
        otpHeading.grid(row=0, column=0, pady=0)
        otpField.grid(row=1, column=0, pady=0)
        resetButton.grid(row=3, column=0, pady=0)
        otpSubmitButton.grid(row=2, column=0, pady=0)
        return
    else:
        messagebox.showerror("Error", response.json()["message"])

def handleButton():
    text = genInput.get("1.0", "end-1c")
    token = ""
    with open("token.txt", "r") as file:
        token = file.read()
    if not token:
        return messagebox.showerror("Error", "Please Logout and Login again")
    if not text:
        return messagebox.showerror("Error", "Please enter a question")    
    def apiCall():
        url = "http://localhost:3000/chatbot"
        code.grid_remove()
        loading.grid(row=2, column=0, pady=0)
        root.update_idletasks()
        try:
            response = requests.post(url, json = {"question":text,"token":token})
            if response.status_code == 200:
                code.grid(row=2, column=0, pady=10, padx=10)
                code.config(state=tk.NORMAL)
                code.delete("1.0", "end")
                resText = response.json()
                cleanText = resText.replace("**","")
                nextCleanText = cleanText.replace("```","")
                code.insert(tk.END,nextCleanText)
                code.config(state=tk.DISABLED)
                loading.grid_remove()
                historyCall()
            else:
                messagebox.showerror("Error", response.json()["message"])
        except Exception as e:
            messagebox.showerror("Error", e)
        finally:
            loading.grid_remove()
    threading.Thread(target=apiCall).start()

def logoutHandler():
    with open("token.txt", "w") as file:
        file.write("")
    python = sys.executable  
    os.execv(python, [python] + sys.argv)

root = tk.Tk()
root.title("Electron")
root.geometry("3000x800")
root.configure(bg="gray87")
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)


headingText = tk.Label(root, text="History", font=('Helvetica', 20,"bold"), bg="gray87", fg="black")
logoutButton = Button(root, height=1,text="Logout", width=5,bgColor="red3", textColor="white",bold=17, 
handleButton=logoutHandler)
genInput = Input(root, textColor="black", bgColor="gray78", width=40)
genButton = Button(root, height=1,text="GO", width=5,bgColor="red3", textColor="white",bold=17, 
handleButton=handleButton )

code = codeArea(root)

loading = tk.Label(root, text="loading...", font=('Helvetica', 20), bg="gray87", fg="black")

text = textArea(root)

historyText = tk.Text(root, wrap=tk.WORD, font=("Courier", 15,"bold"), bg="black", fg="white",width=40 ,padx=25, pady=15)
historyText.config(state=tk.DISABLED)

# getting token from environment variable
token = ""
with open("token.txt","r") as file:
    token = file.read().strip()
if not token:
    # showing the login widgets
    heading = tk.Label(root, bg="gray87", text="SIGN IN", font=("Arial", 34, "bold"))
    emailField = tk.Entry(root, width=30, font=("Helvetica", 25, "bold"), bg="gray80", fg="black")
    submitButton = tk.Button( root,
    text="Submit",
    font=("Arial", 17, "bold"),
    bg="red3",            
    fg="white",
    command=handleSignin,              
    activebackground="red1",   
    activeforeground="white")
    heading.grid(row=0, column=0, pady=0)
    emailField.grid(row=1, column=0, pady=0)
    submitButton.grid(row=2, column=0, pady=0)
else:
    chatbotHandler(genInput, genButton,headingText,logoutButton,code,text,historyText,loading)




root.mainloop()